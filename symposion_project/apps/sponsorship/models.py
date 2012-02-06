import datetime

from django.db import models

from conference.models import Conference


class SponsorLevel(models.Model):
    
    conference = models.ForeignKey(Conference)
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ["conference", "order"]
    
    def __unicode__(self):
        return u"%s %s" % (self.conference, self.name)
    
    def sponsors(self):
        return self.sponsor_set.filter(active=True).order_by("added")


class Sponsor(models.Model):
    
    name = models.CharField(max_length=100)
    external_url = models.URLField("external URL")
    annotation = models.TextField(blank=True)
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField(u"Contact e\u2011mail")
    logo = models.ImageField(upload_to="sponsor_logos/")
    level = models.ForeignKey(SponsorLevel)
    added = models.DateTimeField(default=datetime.datetime.now)
    active = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name
