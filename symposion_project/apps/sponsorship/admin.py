from django.contrib import admin

from sponsorship.models import SponsorLevel, Sponsor


admin.site.register(SponsorLevel)
admin.site.register(Sponsor, list_display=("name", "level", "added", "active"), list_filter = ("level", ))
