from django.db import models

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
