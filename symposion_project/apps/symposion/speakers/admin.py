from django.contrib import admin

from symposion.speakers.models import Speaker


admin.site.register(Speaker,
    list_display = ["name", "email", "twitter_username", "sessions_preference", "created"],
    search_fields = ["name"],
)