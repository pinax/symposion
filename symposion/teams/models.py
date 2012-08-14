import datetime

from django.db import models

import reversion

from django.contrib.auth.models import Permission, User


TEAM_ACCESS_CHOICES = [
    ("open", "open"),
    ("application", "by application"),
    ("invitation", "by invitation")
]


class Team(models.Model):

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    access = models.CharField(max_length=20, choices=TEAM_ACCESS_CHOICES)
    
    # member permissions
    permissions = models.ManyToManyField(Permission, blank=True, related_name="member_teams")
    
    # manager permissions
    manager_permissions = models.ManyToManyField(Permission, blank=True, related_name="manager_teams")
    
    created = models.DateTimeField(default=datetime.datetime.now, editable=False)
    
    @models.permalink
    def get_absolute_url(self):
        return ("team_detail", [self.slug])
    
    def __unicode__(self):
        return self.name

    def get_state_for_user(self, user):
        try:
            return self.memberships.get(user=user).state
        except Membership.DoesNotExist:
            return None
    
    def applicants(self):
        return self.memberships.filter(state="applied")
    
    def invitees(self):
        return self.memberships.filter(state="invited")
    
    def members(self):
        return self.memberships.filter(state="member")
    
    def managers(self):
        return self.memberships.filter(state="manager")


MEMBERSHIP_STATE_CHOICES = [
    ("applied", "applied"),
    ("invited", "invited"),
    ("declined", "declined"),
    ("rejected", "rejected"),
    ("member", "member"),
    ("manager", "manager"),
]


class Membership(models.Model):

    user = models.ForeignKey(User, related_name="memberships")
    team = models.ForeignKey(Team, related_name="memberships")
    state = models.CharField(max_length=20, choices=MEMBERSHIP_STATE_CHOICES)
    message = models.TextField(blank=True)


reversion.register(Membership)
