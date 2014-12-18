from datetime import datetime

from django.db import models


class PublishedPageManager(models.Manager):

        return qs.filter(publish_date__lte=datetime.now())
    def get_queryset(self):
        qs = super(PublishedPageManager, self).get_queryset()
