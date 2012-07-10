from datetime import datetime

from django.db import models

class PublishedPageManager(models.Manager):
    
    def get_query_set(self):
        qs = super(PublishedPageManager, self).get_query_set()
        return qs.filter(publish_date__lte=datetime.now())
