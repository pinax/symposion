import datetime

from django.db import models

from biblion import creole_parser

from symposion.conference.models import PresentationKind


class Proposal(models.Model):
    
    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    AUDIENCE_LEVEL_INTERMEDIATE = 3
    
    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_INTERMEDIATE, "Intermediate"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField(
        max_length = 400, # @@@ need to enforce 400 in UI
        help_text = "Brief one paragraph blurb (will be public if accepted). Must be 400 characters or less"
    )
    kind = models.ForeignKey(PresentationKind)
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
    
    def save(self, *args, **kwargs):
        self.abstract_html = creole_parser.parse(self.abstract)
        super(Proposal, self).save(*args, **kwargs)
    
    def can_edit(self):
        return self.kind in PresentationKind.available()
    
    @property
    def number(self):
        return str(self.pk).zfill(3)
    
    def speakers(self):
        yield self.speaker
        for speaker in self.additional_speakers.all():
            yield speaker
