from django.contrib import admin

from symposion.reviews.models import NotificationTemplate, Review

admin.site.register(Review,
        list_display = ['proposal', 'vote', 'user'],
        list_filter = ['vote',],
        date_heirarchy='submitted_at',
        )



admin.site.register(NotificationTemplate)
