import datetime

from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

from timezones.fields import TimeZoneField


CONFERENCE_CACHE = {}


class Conference(models.Model):
    """
    the full conference for a specific year, e.g. US PyCon 2012.
    """
    
    title = models.CharField(_("title"), max_length=100)
    
    # when the conference runs
    start_date = models.DateField(_("start date"), null=True, blank=True)
    end_date = models.DateField(_("end date"), null=True, blank=True)
    
    # timezone the conference is in
    timezone = TimeZoneField(_("timezone"), blank=True)
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super(Conference, self).save(*args, **kwargs)
        if self.id in CONFERENCE_CACHE:
            del CONFERENCE_CACHE[self.id]
    
    def delete(self):
        pk = self.pk
        super(Conference, self).delete()
        try:
            del CONFERENCE_CACHE[pk]
        except KeyError:
            pass
    
    class Meta(object):
        verbose_name = _("conference")
        verbose_name_plural = _("conferences")


class Section(models.Model):
    """
    a section of the conference such as "Tutorials", "Workshops",
    "Talks", "Expo", "Sprints", that may have its own review and
    scheduling process.
    """
    
    conference = models.ForeignKey(Conference, verbose_name=_("conference"))
    
    name = models.CharField(_("name"), max_length=100)
    
    # when the section runs
    start_date = models.DateField(_("start date"), null=True, blank=True)
    end_date = models.DateField(_("end date"), null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta(object):
        verbose_name = _("section")
        verbose_name_plural = _("sections")


class AudienceLevel(models.Model):
    """
    Sessions, presentations and so on have all a particular target audience.
    Within this target audience you usually have certain levels of experience
    with the topic.

    Most of the there are 3 levels:

    * Novice
    * Intermediate
    * Experienced

    That said, there are sometimes talks that go beyond this by being for
    instance targeted at only people with "Core Contributor" expierence.

    To make custom styling of these levels a bit more flexible, the audience
    level also comes with a slug field for use as CSS-class, while the level
    property is used to sort the audience level.
    """
    conference = models.ForeignKey(Conference, verbose_name=_("conference"))
    name = models.CharField(_("name"), max_length=100)
    slug = models.SlugField(_("slug"))
    level = models.IntegerField(_("level"), blank=True, null=True)

    class Meta(object):
        verbose_name = _("audience level")
        verbose_name_plural = _("audience levels")

    def __unicode__(self):
        return self.name


class SessionDuration(models.Model):
    """
    A conference has usually two kinds of session slot durations. One for
    short talks and one for longer talks. The actual time span varies. Some
    conferences have 20 minutes and 50 minutes respectively, some 15 and 30
    minutes for each session.
    """
    conference = models.ForeignKey(Conference, verbose_name=_("conference"))
    label = models.CharField(_("label"), max_length=100)
    slug = models.SlugField(_("slug"))
    minutes = models.IntegerField(_("minutes"))

    class Meta(object):
        verbose_name = _("session duration")
        verbose_name_plural = _("session durations")

    def __unicode__(self):
        return u"%s (%d min.)" % (self.label, self.minutes)


class SessionKind(models.Model):
    conference = models.ForeignKey(Conference, verbose_name=_("conference"))
    name = models.CharField(_("name"), max_length=50)
    slug = models.SlugField(_("slug"))
    closed = models.NullBooleanField()
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    class Meta(object):
        verbose_name = _("session kind")
        verbose_name_plural = _("session kinds")

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.conference)

    def clean(self):
        """
        A SessionKind can either have neither start nor end date or both.
        """
        super(SessionKind, self).clean()
        if self.closed is None:
            if self.start_date is None or self.end_date is None:
                raise forms.ValidationError(_("You have to specify a start and end date if you leave the 'closed' status undetermined"))
            if self.start_date >= self.end_date:
                raise forms.ValidationError(_("The end date has to be after the start date"))

    def accepts_proposals(self):
        now = datetime.datetime.utcnow()
        if self.conference.start_date is not None:
            if self.conference.start_date < now.date():
                return False
        if self.closed is None:
            return self.start_date <= now <= self.end_date
        return not self.closed


def current_conference():
    from django.conf import settings
    try:
        conf_id = settings.CONFERENCE_ID
    except AttributeError:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured("You must set the CONFERENCE_ID setting.")
    try:
        current_conf = CONFERENCE_CACHE[conf_id]
    except KeyError:
        current_conf = Conference.objects.get(pk=conf_id)
        CONFERENCE_CACHE[conf_id] = current_conf
    return current_conf
