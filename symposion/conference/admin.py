from django.contrib import admin

from symposion.conference.models import Conference, Section


admin.site.register(Conference, list_display=("title", "start_date", "end_date"))
admin.site.register(
    Section,
    prepopulated_fields = {"slug": ("name",)},
    list_display = ("name", "conference", "start_date", "end_date")
)
