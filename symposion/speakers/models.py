import datetime

from django.db import models
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from markitup.fields import MarkupField


class Speaker(models.Model):
    
    user = models.OneToOneField(User, null=True, related_name="speaker_profile")
    name = models.CharField(max_length=100)
    biography = MarkupField()
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
    
    @property
    def email(self):
        if self.user is not None:
            return self.user.email
        else:
            return self.invite_email
