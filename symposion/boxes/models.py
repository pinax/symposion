from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

import reversion

from markitup.fields import MarkupField


@python_2_unicode_compatible
class Box(models.Model):

    label = models.CharField(max_length=100, db_index=True)
    content = MarkupField(blank=True)

    created_by = models.ForeignKey(User, related_name="boxes")
    last_updated_by = models.ForeignKey(User, related_name="updated_boxes")

    def __str__(self):
        return self.label

    class Meta:
        verbose_name_plural = "boxes"


reversion.register(Box)
