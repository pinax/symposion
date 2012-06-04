from django.db import models
from django.contrib.auth.models import User


class Speaker(models.Model):
    user = models.OneToOneField(User, related_name='speaker_profile')

    def __unicode__(self):
        return unicode(self.user)
