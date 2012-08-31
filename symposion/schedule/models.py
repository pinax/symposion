from django.db import models

from markitup.fields import MarkupField

from symposion.proposals.models import ProposalBase
from symposion.conference.models import Section


class Schedule(models.Model):
    
    section = models.OneToOneField(Section)
    slug = models.SlugField(unique=True)


class Day(models.Model):
    
    schedule = models.ForeignKey(Schedule)
    date = models.DateField()
    
    class Meta:
        unique_together = [("schedule", "date")]


class Room(models.Model):
    
    schedule = models.ForeignKey(Schedule)
    name = models.CharField(max_length=65)
    order = models.PositiveIntegerField()


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


class SlotRoom(models.Model):
    """
    Links a slot with a room.
    """
    
    slot = models.ForeignKey(Slot)
    room = models.ForeignKey(Room)
    
    class Meta:
        unique_together = [("slot", "room")]


class Presentation(models.Model):
    
    slot = models.OneToOneField(Slot, null=True, blank=True, related_name="presentation")
    title = models.CharField(max_length=100)
    description = MarkupField()
    abstract = MarkupField()
    speaker = models.ForeignKey("speakers.Speaker", related_name="presentations")
    additional_speakers = models.ManyToManyField("speakers.Speaker", blank=True)
    cancelled = models.BooleanField(default=False)
    _proposal = models.OneToOneField(ProposalBase, related_name="presentation")
    section = models.ForeignKey(Section, related_name="presentations")
    
    @property
    def proposal(self):
        if self._proposal:
            proposal = ProposalBase.objects.get_subclass(pk=self._proposal.pk)
            return proposal
        return None
    
    def speakers(self):
        yield self.speaker
        for speaker in self.additional_speakers.all():
            yield speaker
    
    def __unicode__(self):
        return self.title
