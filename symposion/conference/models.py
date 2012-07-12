from django.db import models
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
    slug = models.SlugField()

    # when the section runs
    start_date = models.DateField(_("start date"), null=True, blank=True)
    end_date = models.DateField(_("end date"), null=True, blank=True)
    
    def __unicode__(self):
        return "%s %s" % (self.conference, self.name)
    
    class Meta(object):
        verbose_name = _("section")
        verbose_name_plural = _("sections")


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
