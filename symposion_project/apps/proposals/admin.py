from django.contrib import admin

from . import models


admin.site.register(models.Proposal,
    list_display=("title", "kind", "conference", "duration"),
    list_filter=("conference", "kind", "duration"))
