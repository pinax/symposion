import datetime

from django.db import models
from django.db.models import Q


class PresentationCategory(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField()
    
    def __unicode__(self):
        return self.name


class PresentationKind(models.Model):
    
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    closed = models.NullBooleanField()
    published = models.NullBooleanField()
    
    @classmethod
    def available(cls):
        now = datetime.datetime.now()
        return cls._default_manager.filter(
            Q(start__lt=now) | Q(start=None),
            Q(end__gt=now) | Q(end=None),
            Q(closed=False) | Q(closed=None),
        )
    
    def __unicode__(self):
        return self.name