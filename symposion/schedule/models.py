import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db import models

from markitup.fields import MarkupField

from symposion.proposals.models import ProposalBase
from symposion.conference.models import Section
from symposion.speakers.models import Speaker


class Schedule(models.Model):

    section = models.OneToOneField(Section)
    published = models.BooleanField(default=True)
    hidden = models.BooleanField("Hide schedule from overall conference view", default=False)

    def __unicode__(self):
        return u"%s Schedule" % self.section

    class Meta:
        ordering = ["section"]


class Day(models.Model):

    schedule = models.ForeignKey(Schedule)
    date = models.DateField()

    def __unicode__(self):
        return u"%s" % self.date

    class Meta:
        unique_together = [("schedule", "date")]
        ordering = ["date"]


class Room(models.Model):

    schedule = models.ForeignKey(Schedule)
    name = models.CharField(max_length=65)
    order = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name


class SlotKind(models.Model):
    """
    A slot kind represents what kind a slot is. For example, a slot can be a
    break, lunch, or X-minute talk.
    """

    schedule = models.ForeignKey(Schedule)
    label = models.CharField(max_length=50)

    def __unicode__(self):
        return self.label


class Slot(models.Model):

    day = models.ForeignKey(Day)
    kind = models.ForeignKey(SlotKind)
    start = models.TimeField()
    end = models.TimeField()
    content_override = MarkupField(blank=True)

    def assign(self, content):
        """
        Assign the given content to this slot and if a previous slot content
        was given we need to unlink it to avoid integrity errors.
        """
        self.unassign()
        content.slot = self
        content.save()

    def unassign(self):
        """
        Unassign the associated content with this slot.
        """
        content = self.content
        if content and content.slot_id:
            content.slot = None
            content.save()

    @property
    def content(self):
        """
        Return the content this slot represents.
        @@@ hard-coded for presentation for now
        """
        try:
            return self.content_ptr
        except ObjectDoesNotExist:
            return None

    @property
    def start_datetime(self):
        return datetime.datetime(
            self.day.date.year,
            self.day.date.month,
            self.day.date.day,
            self.start.hour,
            self.start.minute)

    @property
    def end_datetime(self):
        return datetime.datetime(
            self.day.date.year,
            self.day.date.month,
            self.day.date.day,
            self.end.hour,
            self.end.minute)

    @property
    def length_in_minutes(self):
        return int(
            (self.end_datetime - self.start_datetime).total_seconds() / 60)

    @property
    def rooms(self):
        return Room.objects.filter(pk__in=self.slotroom_set.values("room"))

    def __unicode__(self):
        roomlist = ' '.join(map(lambda r: r.__unicode__(), self.rooms))
        return u"%s %s (%s - %s) %s" % (self.day, self.kind, self.start, self.end, roomlist)

    class Meta:
        ordering = ["day", "start", "end"]


class SlotRoom(models.Model):
    """
    Links a slot with a room.
    """

    slot = models.ForeignKey(Slot)
    room = models.ForeignKey(Room)

    def __unicode__(self):
        return u"%s %s" % (self.room, self.slot)

    class Meta:
        unique_together = [("slot", "room")]
        ordering = ["slot", "room__order"]


class Presentation(models.Model):

    slot = models.OneToOneField(Slot, null=True, blank=True, related_name="content_ptr")
    title = models.CharField(max_length=100)
    description = MarkupField()
    abstract = MarkupField()
    speaker = models.ForeignKey(Speaker, related_name="presentations")
    additional_speakers = models.ManyToManyField(Speaker, related_name="copresentations",
                                                 blank=True)
    cancelled = models.BooleanField(default=False)
    proposal_base = models.OneToOneField(ProposalBase, related_name="presentation")
    section = models.ForeignKey(Section, related_name="presentations")

    @property
    def number(self):
        return self.proposal.number

    @property
    def proposal(self):
        if self.proposal_base_id is None:
            return None
        return ProposalBase.objects.get_subclass(pk=self.proposal_base_id)

    def speakers(self):
        yield self.speaker
        for speaker in self.additional_speakers.all():
            if speaker.user:
                yield speaker

    def __unicode__(self):
        return u"#%s %s (%s)" % (self.number, self.title, self.speaker)

    class Meta:
        ordering = ["slot"]


class Session(models.Model):

    day = models.ForeignKey(Day, related_name="sessions")
    slots = models.ManyToManyField(Slot, related_name="sessions")

    def sorted_slots(self):
        return self.slots.order_by("start")

    def start(self):
        slots = self.sorted_slots()
        if slots:
            return list(slots)[0].start
        else:
            return None

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
            return u"%s: %s - %s" % (
                self.day.date.strftime("%a"),
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

    submitted = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        unique_together = [("session", "user", "role")]

    def __unicode__(self):
        return u"%s %s: %s" % (self.user, self.session,
                               self.SESSION_ROLE_TYPES[self.role - 1][1])
