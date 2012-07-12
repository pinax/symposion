import datetime

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from symposion.conference.models import Conference

from symposion.sponsorship.managers import SponsorManager


class SponsorLevel(models.Model):
    
    conference = models.ForeignKey(Conference, verbose_name=_("conference"))
    name = models.CharField(_("name"), max_length=100)
    order = models.IntegerField(_("order"), default=0)
    cost = models.PositiveIntegerField(_("cost"))
    description = models.TextField(_("description"), blank=True, help_text=_("This is private."))
    
    class Meta:
        ordering = ["conference", "order"]
        verbose_name = _("sponsor level")
        verbose_name_plural = _("sponsor levels")
    
    def __unicode__(self):
        return u"%s %s" % (self.conference, self.name)
    
    def sponsors(self):
        return self.sponsor_set.filter(active=True).order_by("added")


class Sponsor(models.Model):
    
    applicant = models.ForeignKey(User, related_name="sponsorships", verbose_name=_("applicant"), null=True)
    
    name = models.CharField(_("Sponsor Name"), max_length=100)
    external_url = models.URLField(_("external URL"))
    annotation = models.TextField(_("annotation"), blank=True)
    contact_name = models.CharField(_("Contact Name"), max_length=100)
    contact_email = models.EmailField(_(u"Contact Email"))
    level = models.ForeignKey(SponsorLevel, verbose_name=_("level"))
    added = models.DateTimeField(_("added"), default=datetime.datetime.now)
    active = models.BooleanField(_("active"), default=False)
    
    # Denormalization (this assumes only one logo)
    sponsor_logo = models.ForeignKey("SponsorBenefit", related_name="+", null=True, blank=True, editable=False)

    objects = SponsorManager()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _("sponsor")
        verbose_name_plural = _("sponsors")
    
    def get_absolute_url(self):
        if self.active:
            return reverse("sponsor_detail", kwargs={"pk": self.pk})
        return reverse("sponsor_list")


BENEFIT_TYPE_CHOICES = [
    ("text", "Text"),
    ("file", "File"),
    ("weblogo", "Web Logo"),
    ("simple", "Simple")
]


class Benefit(models.Model):
    
    name = models.CharField(_("name"), max_length=100)
    description = models.TextField(_("description"), blank=True)
    type = models.CharField(_("type"), choices=BENEFIT_TYPE_CHOICES, max_length=10, default="simple")
    
    def __unicode__(self):
        return self.name


class BenefitLevel(models.Model):
    
    benefit = models.ForeignKey(Benefit, related_name="benefit_levels", verbose_name=_("benefit"))
    level = models.ForeignKey(SponsorLevel, related_name="benefit_levels", verbose_name=_("level"))

    # default limits for this benefit at given level
    max_words = models.PositiveIntegerField(_("max words"), blank=True, null=True)
    other_limits = models.CharField(_("other limits"), max_length=200, blank=True)
    
    class Meta:
        ordering = ["level"]
    
    def __unicode__(self):
        return u"%s - %s" % (self.level, self.benefit)


class SponsorBenefit(models.Model):
    
    sponsor = models.ForeignKey(Sponsor, related_name="sponsor_benefits", verbose_name=_("sponsor"))
    benefit = models.ForeignKey(Benefit, related_name="sponsor_benefits", verbose_name=_("benefit"))
    active = models.BooleanField(default=True)
    
    # Limits: will initially be set to defaults from corresponding BenefitLevel
    max_words = models.PositiveIntegerField(_("max words"), blank=True, null=True)
    other_limits = models.CharField(_("other limits"), max_length=200, blank=True)
    
    # Data: zero or one of these fields will be used, depending on the
    # type of the Benefit (text, file, or simple)
    text = models.TextField(_("text"), blank=True)
    upload = models.FileField(_("file"), blank=True, upload_to="sponsor_files")
    
    class Meta:
        ordering = ['-active']
    
    def __unicode__(self):
        return u"%s - %s" % (self.sponsor, self.benefit)
    
    def clean(self):
        if self.max_words and len(self.text.split()) > self.max_words:
            raise ValidationError("Sponsorship level only allows for %s words." % self.max_words)
    
    def data_fields(self):
        """
        Return list of data field names which should be editable for
        this ``SponsorBenefit``, depending on its ``Benefit`` type.
        """
        if self.benefit.type == "file" or self.benefit.type == "weblogo":
            return ["upload"]
        elif self.benefit.type == "text":
            return ["text"]
        return []
