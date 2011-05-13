import datetime

from django.db import models


class SponsorLevel(models.Model):
    
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    description = models.TextField(blank=True, help_text="This is private.")
    
    class Meta:
        ordering = ["order"]
    
    def __unicode__(self):
        return self.name


class Sponsor(models.Model):
    
    name = models.CharField(max_length=100)
    external_url = models.URLField("external URL")
    annotation = models.TextField(blank=True)
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField(u"Contact e\u2011mail")
    level = models.ForeignKey(SponsorLevel)
    added = models.DateTimeField(default=datetime.datetime.now)
    active = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name
    
    @property
    def website_logo(self):
        try:
            logo = SponsorLogo.objects.get(sponsor=self, label="website")
        except SponsorLogo.DoesNotExist:
            return None
        else:
            return logo.logo


class SponsorLogo(models.Model):
    
    sponsor = models.ForeignKey(Sponsor)
    label = models.CharField(
        max_length = 100,
        help_text = "To display this logo on site use label 'website'"
    )
    logo = models.ImageField(upload_to="sponsor_logos/")
    
    class Meta:
        unique_together = [("sponsor", "label")]
