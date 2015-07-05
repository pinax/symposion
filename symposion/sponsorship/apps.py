from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class SponsorshipConfig(AppConfig):
    name = "symposion.sponsorship"
    label = "symposion_sponsorship"
    verbose_name = _("Symposion Sponsorship")
