from __future__ import unicode_literals
from django.contrib import admin

from symposion.speakers.models import speaker_model


admin.site.register(speaker_model(),
                    list_display=["name", "email", "created"],
                    search_fields=["name"])
