from django.contrib import admin

from symposion.sponsors.models import SponsorLevel, Sponsor, SponsorLogo


class SponsorLogoInline(admin.StackedInline):
    model = SponsorLogo
    extra = 1


admin.site.register(SponsorLevel)
admin.site.register(Sponsor,
    inlines = [
        SponsorLogoInline
    ]
)