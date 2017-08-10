from __future__ import unicode_literals

import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from model_utils.managers import InheritanceManager

from symposion.markdown_parser import parse
from symposion.utils.loader import object_from_settings


def speaker_model():
    default = "symposion.speakers.models.DefaultSpeaker"
    return object_from_settings("SYMPOSION_SPEAKER_MODEL", default)


@python_2_unicode_compatible
class SpeakerBase(models.Model):
    ''' Base class for conference speaker profiles. This model is not meant to
    be used directly; it merely contains the default fields that every
    conference would want. You should instead subclass this model.
    DefaultSpeaker is a minimal subclass that may be useful. '''

    objects = InheritanceManager()


    def subclass(self):
        ''' Returns the subclassed version of this model '''

        try:
            # The cached subclass instance so we don't need to query frequently
            return self.__subclass_instance__
        except AttributeError:
            instance = self.__class__.objects.get_subclass(id=self.id)
            if type(instance) == type(self):
                instance = self
            self.__subclass_instance__ = instance
            return instance

    def __getattr__(self, attr):
        ''' Overrides getattr to allow us to return subclass properties
        from the base class. '''

        try:
            return super(SpeakerBase, self).__getattr__(attr)
        except AttributeError:
            if attr == "__subclass_instance__":
                raise
            subclass = self.subclass()
            return getattr(subclass, attr)

    user = models.OneToOneField(User, null=True, related_name="speaker_profile", verbose_name=_("User"))
    name = models.CharField(verbose_name=_("Name"), max_length=100,
                            help_text=_("As you would like it to appear in the"
                                        " conference program."))
    biography = models.TextField(blank=True, help_text=_("A little bit about you.  Edit using "
                                                         "<a href='http://warpedvisions.org/projects/"
                                                         "markdown-cheat-sheet/target='_blank'>"
                                                         "Markdown</a>."), verbose_name=_("Biography"))
    biography_html = models.TextField(blank=True)
    photo = models.ImageField(upload_to="speaker_photos", blank=True, verbose_name=_("Photo"))
    annotation = models.TextField(verbose_name=_("Annotation"))  # staff only
    invite_email = models.CharField(max_length=200, unique=True, null=True, db_index=True, verbose_name=_("Invite_email"))
    invite_token = models.CharField(max_length=40, db_index=True, verbose_name=_("Invite token"))
    created = models.DateTimeField(
        default=datetime.datetime.now,
        editable=False,
        verbose_name=_("Created")
    )

    class Meta:
        ordering = ['name']
        verbose_name = _("Speaker")
        verbose_name_plural = _("Speakers")

    def save(self, *args, **kwargs):
        self.biography_html = parse(self.biography)
        return super(SpeakerBase, self).save(*args, **kwargs)

    def __str__(self):
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

    @property
    def all_presentations(self):
        presentations = []
        if self.presentations:
            for p in self.presentations.all():
                presentations.append(p)
            for p in self.copresentations.all():
                presentations.append(p)
        return presentations


#@python_2_unicode_compatible
class DefaultSpeaker(SpeakerBase):

    def clean_twitter_username(self):
        value = self.twitter_username
        if value.startswith("@"):
            value = value[1:]
        return value

    def save(self, *args, **kwargs):
        self.twitter_username = self.clean_twitter_username()
        return super(DefaultSpeaker, self).save(*args, **kwargs)

    twitter_username = models.CharField(
        max_length=15,
        blank=True,
        help_text=_(u"Your Twitter account")
    )
