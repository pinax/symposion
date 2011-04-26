import datetime

from django.db import models
from django.db.models import Q

from biblion import creole_parser


class ProposalSessionType(models.Model):
    
    name = models.CharField(max_length=100)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    closed = models.NullBooleanField()
    
    @classmethod
    def available(cls):
        now = datetime.datetime.now()
        return cls._default_manager.filter(
            Q(start__lt=now) | Q(start=None),
            Q(end__gt=now) | Q(end=None),
            Q(closed=False) | Q(closed=None),
        )
    
    def __unicode__(self):
        return self.name


class Proposal(models.Model):
    
    SESSION_TYPE_TALK = 1
    SESSION_TYPE_PANEL = 2
    SESSION_TYPE_TUTORIAL = 3
    SESSION_TYPE_POSTER = 4
    
    SESSION_TYPES = [
        (SESSION_TYPE_TALK, "Talk"),
        (SESSION_TYPE_PANEL, "Panel"),
        (SESSION_TYPE_TUTORIAL, "Tutorial"),
        (SESSION_TYPE_POSTER, "Poster")
    ]
    
    SESSION_CLASSIFICATION_SURVEY = 1
    SESSION_CLASSIFICATION_RAISE_AWARENESS = 2
    SESSION_CLASSIFICATION_INDEPTH = 3
    
    SESSION_CLASSIFICATIONS = [
        (SESSION_CLASSIFICATION_SURVEY, "Survey"),
        (SESSION_CLASSIFICATION_RAISE_AWARENESS, "Raise Awareness"),
        (SESSION_CLASSIFICATION_INDEPTH, "Discuss in Depth"),
    ]
    
    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    
    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField(
        max_length = 400, # @@@ need to enforce 400 in UI
        help_text = "Brief one paragraph blurb (will be public if accepted). Must be 400 characters or less"
    )
    session_type = models.IntegerField(choices=SESSION_TYPES)
    classification = models.IntegerField(choices=SESSION_CLASSIFICATIONS)
    abstract = models.TextField(
        help_text = "More detailed description (will be public if accepted). You can use <a href='http://wikicreole.org/' target='_blank'>creole</a> markup. <a id='preview' href='#'>Preview</a>",
    )
    abstract_html = models.TextField(editable=False)
    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)
    additional_notes = models.TextField(
        blank=True,
        help_text = "Anything else you'd like the program committee to know when making their selection: your past speaking experience, open source community experience, etc."
    )
    submitted = models.DateTimeField(
        default = datetime.datetime.now,
        editable = False,
    )
    speaker = models.ForeignKey("speakers.Speaker", related_name="proposals")
    additional_speakers = models.ManyToManyField("speakers.Speaker", blank=True)
    cancelled = models.BooleanField(default=False)
    
    # PyCon additions
    recording = models.BooleanField(
        default=True,
        help_text="I grant permission for PyCon to record my talk in audio and video and make these recordings publicly available."
    )
    opt_out_ads = models.NullBooleanField(default=False)
    extreme_pycon = models.BooleanField(
        u"EXTREME PyCon!",
        default=False,
        help_text="This talk will skip the intro fluff, assume the audience has the needed background, and dive straight into the details."
    )
    invited = models.BooleanField(
        default=False,
    )
    
    def save(self, *args, **kwargs):
        self.abstract_html = creole_parser.parse(self.abstract)
        super(Proposal, self).save(*args, **kwargs)
    
    def can_edit(self):
        return self.get_session_type_display() in [pst.name for pst in ProposalSessionType.available()]
    
    @property
    def number(self):
        return str(self.pk).zfill(3)
    
    def speakers(self):
        yield self.speaker
        for speaker in self.additional_speakers.all():
            yield speaker
