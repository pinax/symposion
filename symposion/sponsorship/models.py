import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from conference.models import Conference


class SponsorLevel(models.Model):
    
    conference = models.ForeignKey(Conference, verbose_name=_("conference"))
    name = models.CharField(_("name"), max_length=100)
    order = models.IntegerField(_("order"), default=0)
    description = models.TextField(_("description"), blank=True)
    
    class Meta:
        ordering = ["conference", "order"]
        verbose_name = _("sponsor level")
        verbose_name_plural = _("sponsor levels")
    
    def __unicode__(self):
        return u"%s %s" % (self.conference, self.name)
    
    def sponsors(self):
        return self.sponsor_set.filter(active=True).order_by("added")


class Sponsor(models.Model):
    
    name = models.CharField(_("name"), max_length=100)
    external_url = models.URLField(_("external URL"))
    annotation = models.TextField(_("annotation"), blank=True)
    contact_name = models.CharField(_("contact_name"), max_length=100)
    contact_email = models.EmailField(_(u"Contact e\u2011mail"))
    logo = models.ImageField(_("logo"), upload_to="sponsor_logos/")
    level = models.ForeignKey(SponsorLevel, verbose_name=_("level"))
    added = models.DateTimeField(_("added"), default=datetime.datetime.now)
    active = models.BooleanField(_("active"), default=False)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _("sponsor")
        verbose_name_plural = _("sponsors")
