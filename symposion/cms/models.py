import datetime
import os
import re

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from markitup.fields import MarkupField

from taggit.managers import TaggableManager

import reversion

from .managers import PublishedPageManager


class Page(models.Model):
    
    STATUS_CHOICES = (
        (1, _("Draft")),
        (2, _("Public")),
    )
    
    title = models.CharField(max_length=100)
    path = models.CharField(max_length=100, unique=True)
    body = MarkupField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=2)
    publish_date = models.DateTimeField(default=datetime.datetime.now)
    created = models.DateTimeField(editable=False, default=datetime.datetime.now)
    updated = models.DateTimeField(editable=False, default=datetime.datetime.now)
    tags = TaggableManager(blank=True)
    
    published = PublishedPageManager()
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ("cms_page", [self.path])
    
    def save(self, *args, **kwargs):
        self.updated = datetime.datetime.now()
        super(Page, self).save(*args, **kwargs)
    
    def clean_fields(self, exclude=None):
        super(Page, self).clean_fields(exclude)
        if not re.match(settings.SYMPOSION_PAGE_REGEX, self.path):
            raise ValidationError({"path": [_("Path can only contain letters, numbers and hyphens and end with /")]})


reversion.register(Page)


def generate_filename(instance, filename):
    return filename


class File(models.Model):
    
    file = models.FileField(upload_to=generate_filename)
    created = models.DateTimeField(default=datetime.datetime.now)
    
    def download_url(self):
        return reverse("file_download", args=[self.pk, os.path.basename(self.file.name).lower()])
