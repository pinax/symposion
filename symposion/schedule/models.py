from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from markitup.fields import MarkupField
from model_utils.managers import InheritanceManager

from symposion.proposals.models import ProposalBase
from symposion.conference.models import Section


class Schedule(models.Model):
    
    section = models.OneToOneField(Section)


class Day(models.Model):
    
    schedule = models.ForeignKey(Schedule)
    date = models.DateField()
    
    class Meta:
        unique_together = [("schedule", "date")]


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


class Slot(models.Model):
    
    day = models.ForeignKey(Day)
    kind = models.ForeignKey(SlotKind)
    start = models.TimeField()
    end = models.TimeField()
    content_override = models.TextField(blank=True)
    
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
        if self.content and self.content.slot_id:
            self.content.slot = None
            self.content.save()
    
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
    def rooms(self):
        return Room.objects.filter(pk__in=self.slotroom_set.values("room"))


class SlotRoom(models.Model):
    """
    Links a slot with a room.
    """
    
    slot = models.ForeignKey(Slot)
    room = models.ForeignKey(Room)
    
    class Meta:
        unique_together = [("slot", "room")]


class Presentation(models.Model):
    
    slot = models.OneToOneField(Slot, null=True, blank=True, related_name="content_ptr")
    title = models.CharField(max_length=100)
    description = MarkupField()
    abstract = MarkupField()
    speaker = models.ForeignKey("speakers.Speaker", related_name="presentations")
    additional_speakers = models.ManyToManyField("speakers.Speaker", blank=True)
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
            yield speaker
    
    def __unicode__(self):
        return "#%s %s (%s)" % (self.number, self.title, self.speaker)
