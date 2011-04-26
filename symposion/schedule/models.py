# encoding: utf-8
import datetime

from django.db import models

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from biblion import creole_parser


class Track(models.Model):
    
    name = models.CharField(max_length=65)
    
    def __unicode__(self):
        return self.name


class Session(models.Model):
    
    track = models.ForeignKey(Track, null=True, related_name="sessions")
    
    def sorted_slots(self):
        ct = ContentType.objects.get_for_model(Presentation)
        return self.slots.filter(kind=ct).order_by("start")
    
    # @@@ cache?
    def start(self):
        slots = self.sorted_slots()
        if slots:
            return list(slots)[0].start
        else:
            return None
    
    # @@@ cache?
    def end(self):
        slots = self.sorted_slots()
        if slots:
            return list(slots)[-1].end
        else:
            return None
    
    def __unicode__(self):
        start = self.start()
        end = self.end()
        if start and end:
            return u"%s: %s — %s" % (
                start.strftime("%a"),
                start.strftime("%X"),
                end.strftime("%X")
            )
        return u""


class SessionRole(models.Model):
    
    SESSION_ROLE_CHAIR = 1
    SESSION_ROLE_RUNNER = 2
    
    SESSION_ROLE_TYPES = [
        (SESSION_ROLE_CHAIR, "Session Chair"),
        (SESSION_ROLE_RUNNER, "Session Runner"),
    ]
    
    session = models.ForeignKey(Session)
    user = models.ForeignKey(User)
    role = models.IntegerField(choices=SESSION_ROLE_TYPES)
    status = models.NullBooleanField()
    
    submitted = models.DateTimeField(default = datetime.datetime.now)
    
    class Meta:
        unique_together = [("session", "user", "role")]


# @@@ precreate the Slots with proposal == None and then making the schedule is just updating slot.proposal and/or title/notes
class Slot(models.Model):
    
    title = models.CharField(max_length=100, null=True, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    kind = models.ForeignKey(ContentType, null=True, blank=True)
    track = models.ForeignKey(Track, null=True, blank=True, related_name="slots")
    session = models.ForeignKey(Session, null=True, blank=True, related_name="slots")
    
    def content(self):
        if self.kind_id:
            return self.kind.get_object_for_this_type(slot=self)
        else:
            return None
    
    def assign(self, content, old_content=None):
        if old_content is not None:
            old_content.slot = None
            old_content.save()
        content.slot = self
        content.save()
        self.kind = ContentType.objects.get_for_model(content)
        self.save()
    
    def unassign(self):
        content = self.content()
        content.slot = None
        content.save()
        self.kind = None
        self.save()
    
    def __unicode__(self):
        return u"%s: %s — %s" % (self.start.strftime("%a"), self.start.strftime("%X"), self.end.strftime("%X"))


class Presentation(models.Model):
    
    PRESENTATION_TYPE_TALK = 1
    PRESENTATION_TYPE_PANEL = 2
    PRESENTATION_TYPE_TUTORIAL = 3
    PRESENTATION_TYPE_POSTER = 4
    
    PRESENTATION_TYPES = [
        (PRESENTATION_TYPE_TALK, "Talk"),
        (PRESENTATION_TYPE_PANEL, "Panel"),
        (PRESENTATION_TYPE_TUTORIAL, "Tutorial"),
        (PRESENTATION_TYPE_POSTER, "Poster")
    ]
    
    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_EXPERIENCED = 2
    
    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Novice"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Experienced"),
    ]
    
    slot = models.OneToOneField(Slot, null=True, blank=True, related_name="presentation")
    
    title = models.CharField(max_length=100)
    description = models.TextField(
        max_length = 400, # @@@ need to enforce 400 in UI
        help_text = "Brief one paragraph blurb (will be public if accepted). Must be 400 characters or less"
    )
    presentation_type = models.IntegerField(choices=PRESENTATION_TYPES)
    abstract = models.TextField(
        help_text = "More detailed description (will be public if accepted). You can use <a href='http://wikicreole.org/' target='_blank'>creole</a> markup. <a id='preview' href='#'>Preview</a>",
    )
    abstract_html = models.TextField(editable=False)
    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)
    
    submitted = models.DateTimeField(
        default = datetime.datetime.now,
        editable = False,
    )
    speaker = models.ForeignKey("speakers.Speaker", related_name="sessions")
    additional_speakers = models.ManyToManyField("speakers.Speaker", blank=True)
    cancelled = models.BooleanField(default=False)
    
    extreme_pycon = models.BooleanField(u"EXTREME PyCon!", default=False)
    invited = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.abstract_html = creole_parser.parse(self.abstract)
        super(Presentation, self).save(*args, **kwargs)
    
    def speakers(self):
        yield self.speaker
        for speaker in self.additional_speakers.all():
            yield speaker
    
    def __unicode__(self):
        return u"%s" % self.title


class Plenary(models.Model):
    
    slot = models.OneToOneField(Slot, null=True, blank=True, related_name="plenary")
    title = models.CharField(max_length=100)
    speaker = models.ForeignKey("speakers.Speaker", null=True, blank=True, related_name="+")
    additional_speakers = models.ManyToManyField("speakers.Speaker", blank=True)
    description = models.TextField(max_length=400, blank=True)


class Recess(models.Model):
    """
    We call this recess due to Break resulting in using break (lower-case "b")
    which is a Python keyword.
    """
    
    slot = models.OneToOneField(Slot, null=True, blank=True, related_name="recess")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=400, blank=True)


class UserBookmark(models.Model):
    
    user = models.ForeignKey(User)
    presentation = models.ForeignKey(Presentation)
    
    class Meta:
        unique_together = [("user", "presentation")]
