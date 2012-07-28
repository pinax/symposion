import datetime

from django.db import models

import reversion

from django.contrib.auth.models import Permission, User


TEAM_ACCESS_CHOICES = [
    (1, "open"),
    (2, "by application"),
    (3, "by invitation")
]


class Team(models.Model):

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    access = models.IntegerField(choices=TEAM_ACCESS_CHOICES)
    permissions = models.ManyToManyField(Permission, blank=True)
    created = models.DateTimeField(default=datetime.datetime.now, editable=False)
    
    def __unicode__(self):
        return self.name


MEMBERSHIP_STATE_CHOICES = [
    (1, "applied"),
    (2, "invited"),
    (3, "declined"),
    (4, "rejected"),
    (5, "member"),
    (6, "manager"),
]


class Membership(models.Model):

    user = models.ForeignKey(User)
    team = models.ForeignKey(Team)
    state = models.IntegerField(choices=MEMBERSHIP_STATE_CHOICES)
    message = models.TextField(blank=True)


reversion.register(Membership)
