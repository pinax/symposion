from django.db import models

from timezones.fields import TimeZoneField


class Conference(models.Model):
    """
    the full conference for a specific year, e.g. US PyCon 2012.
    """
    
    title = models.CharField(max_length=100)
    
    # when the conference runs
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    # timezone the conference is in
    timezone = TimeZoneField(blank=True)
    
    def __unicode__(self):
        return self.title


class Section(models.Model):
    """
    a section of the conference such as "Tutorials", "Workshops",
    "Talks", "Expo", "Sprints", that may have its own review and
    scheduling process.
    """
    
    conference = models.ForeignKey(Conference)
    
    name = models.CharField(max_length=100)
    
    # when the section runs
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name
