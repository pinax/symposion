from django.contrib import admin

from symposion.speakers.models import Speaker


admin.site.register(Speaker,
    list_display = ["name", "twitter_username", "created"],
)