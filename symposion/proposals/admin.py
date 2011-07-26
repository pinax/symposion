from django.contrib import admin

from symposion.proposals.models import Proposal


admin.site.register(Proposal,
    list_display = [
        "title",
        "kind",
        "audience_level",
        "cancelled",
    ]
)