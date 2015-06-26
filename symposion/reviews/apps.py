from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ReviewsConfig(AppConfig):
    name = "symposion.reviews"
    label = "symposion_reviews"
    verbose_name = _("Symposion Reviews")
