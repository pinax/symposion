import datetime

from django.db import models
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from markitup.fields import MarkupField


class Speaker(models.Model):
    
    SESSION_COUNT_CHOICES = [
        (1, "One"),
        (2, "Two")
    ]
    
    user = models.OneToOneField(User, null=True, related_name="speaker_profile")
    name = models.CharField(max_length=100, help_text="As you would like it to appear in the conference program.")
    biography = MarkupField(blank=True, help_text="A little bit about you. Edit using <a href='http://warpedvisions.org/projects/markdown-cheat-sheet/' target='_blank'>Markdown</a>.")
    photo = models.ImageField(upload_to="speaker_photos", blank=True)
    annotation = models.TextField()  # staff only
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
