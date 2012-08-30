from django.db import models

from symposion.conference.models import Section
from symposion.schedule.utils import InlineSet


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
    room_set = models.TextField(db_column="rooms")
    kind = models.ForeignKey(SlotKind)
    start = models.TimeField()
    end = models.TimeField()
    
    @property
    def rooms(self):
        attr = "_rooms"
        if not hasattr(self, attr):
            class RoomInlineSet(InlineSet):
                def consective_count(self):
                    return len(self)
            value = RoomInlineSet(obj=self, field="room_set", delimiter=" ")
            setattr(self, attr, value)
        return getattr(self, attr)
