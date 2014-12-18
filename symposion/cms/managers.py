from django.utils import timezone

from django.db import models


class PublishedPageManager(models.Manager):

    def get_queryset(self):
        qs = super(PublishedPageManager, self).get_queryset()
        return qs.filter(publish_date__lte=timezone.now())
