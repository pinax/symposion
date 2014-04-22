from django.contrib import admin

from symposion.reviews.models import NotificationTemplate, Review

admin.site.register(Review,
        list_display = ['proposal', 'section', 'vote', 'user'],
        list_filter = ['vote', 'section'],
        date_heirarchy='submitted_at',
        )



admin.site.register(NotificationTemplate)
