import datetime
from itertools import chain

from django.db import models
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from biblion import creole_parser


class Speaker(models.Model):
    
    user = models.OneToOneField(User, null=True, related_name="speaker_profile")
    name = models.CharField(max_length=100)
    biography = models.TextField(
        help_text = "You can use <a href='http://wikicreole.org/' target='_blank'>creole</a> markup. <a id='preview' href='#'>Preview</a>",
    )
    biography_html = models.TextField(editable=False)
    photo = models.ImageField(upload_to="speaker_photos", blank=True)
    twitter_username = models.CharField(max_length=15, blank=True)
    annotation = models.TextField() # staff only
    invite_email = models.CharField(max_length=200, unique=True, null=True, db_index=True)
    invite_token = models.CharField(max_length=40, db_index=True)
    created = models.DateTimeField(
        default = datetime.datetime.now,
        editable = False
    )
    
    def __unicode__(self):
        if self.user:
            return self.name
        else:
            return "?"
    
    def get_absolute_url(self):
        return reverse("speaker_edit")
    
    def save(self, *args, **kwargs):
        self.biography_html = creole_parser.parse(self.biography)
        super(Speaker, self).save(*args, **kwargs)
    
    @property
    def presentations(self):
        # schedule may not be installed so we need to check for sessions
        if hasattr(self, "sessions"):
            sessions = self.sessions.exclude(slot=None)
            additional_sessions = self.presentation_set.exclude(slot=None)
            return list(chain(sessions, additional_sessions))
        return None
    
    @property
    def email(self):
        if self.user is not None:
            return self.user.email
        else:
            return self.invite_email
