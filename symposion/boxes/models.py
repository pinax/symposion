from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

import reversion

from markitup.fields import MarkupField


@python_2_unicode_compatible
class Box(models.Model):

    label = models.CharField(max_length=100, db_index=True, verbose_name=_("Label"))
    content = MarkupField(blank=True)

    created_by = models.ForeignKey(User, related_name="boxes", verbose_name=_("Created by"))
    last_updated_by = models.ForeignKey(User, related_name="updated_boxes", verbose_name=_("Last updated by"))

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = _("Box")
        verbose_name_plural = _("Boxes")

reversion.register(Box)
