from django.db import models

from symposion.conference.models import Section


class Schedule(models.Model):
    
    section = models.OneToOneField(Section)


class Day(models.Model):
    
    date = models.DateField()


class Track(models.Model):
    
    name = models.CharField(max_length=65)
    room = models.CharField(max_length=100)


class Slot(models.Model):
    
    day = models.ForeignKey(Day)
    track_set = models.TextField(db_column="tracks")
    start = models.TimeField()
    end = models.TimeField()
    
    @property
    def tracks(self):
        attr = "_tracks"
        if not hasattr(self, attr):
            slot = self
            class TrackSet(object):
                
                def __init__(self, data, delimiter):
                    self.data = set(data.split(delimiter))
                
                def __iter__(self):
                    return Track.objects.filter(pk__in=self.data)
                
                def add(self, track, commit=True):
                    """
                    Add given track to the set, but check if it can exist
                    before adding it.
                    """
                    self.data.add(track.pk)
                    self._update_model(commit=commit)
                
                def remove(self, track, commit=True):
                    self.data.remove(track.pk)
                    self._update_model(commit=commit)
                
                def _update_model(self, commit=True):
                    slot.track_set += self.delimiter.join(self.data)
                    if commit:
                        slot.save(force_update=True)
            setattr(self, attr, TrackSet(self.track_set, delimiter=" "))
        return getattr(self, attr)
