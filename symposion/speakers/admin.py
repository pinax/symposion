from __future__ import unicode_literals
from django.contrib import admin

from symposion.speakers.models import DefaultSpeaker

# TODO: Allow DefaultSpeaker to be switched off in admin.
admin.site.register(DefaultSpeaker,
                    list_display=["name", "email", "created", "twitter_username"],
                    search_fields=["name"])
