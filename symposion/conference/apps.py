from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ConferenceConfig(AppConfig):
    name = "symposion.conference"
    label = "symposion_conference"
    verbose_name = _("Symposion Conference")
