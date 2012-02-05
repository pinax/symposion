from django.contrib import admin

from symposion.sponsors.models import SponsorLevel, Sponsor


admin.site.register(SponsorLevel)
admin.site.register(Sponsor)
