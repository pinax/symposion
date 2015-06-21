from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from symposion.sponsorship.models import SponsorLevel, Sponsor, Benefit, \
    BenefitLevel, SponsorBenefit
from symposion.sponsorship.views import sponsor_email


class BenefitLevelInline(admin.TabularInline):
    model = BenefitLevel
    extra = 0


class SponsorBenefitInline(admin.StackedInline):
    model = SponsorBenefit
    extra = 0
    fieldsets = [
        (None, {
            "fields": [
                ("benefit", "active"),
                ("max_words", "other_limits"),
                "text",
                "upload",
            ]
        })
    ]


def email_selected_sponsors_action(modeladmin, request, queryset):
    """Action invoked from admin to email selected sponsors"""
    pks = ",".join([str(pk) for pk in queryset.values_list('pk', flat=True)])
    return sponsor_email(request, pks)
email_selected_sponsors_action.short_description = _(u"Email selected sponsors")


class SponsorAdmin(admin.ModelAdmin):

    save_on_top = True
    actions = [email_selected_sponsors_action]
    list_per_page = 1000000  # Do not limit sponsors per page, just one big page
    fieldsets = [
        (None, {
            "fields": [
                ("name", "applicant"),
                ("level", "active"),
                "external_url",
                "annotation",
                ("contact_name", "contact_email")
            ]
        }),
        ("Metadata", {
            "fields": ["added"],
            "classes": ["collapse"]
        })
    ]
    inlines = [SponsorBenefitInline]
    list_display = ["name", "external_url", "level", "active"]
    ordering = ["active", "level", "name"]

    def get_form(self, *args, **kwargs):
        # @@@ kinda ugly but using choices= on NullBooleanField is broken
        form = super(SponsorAdmin, self).get_form(*args, **kwargs)
        form.base_fields["active"].widget.choices = [
            (u"1", "unreviewed"),
            (u"2", "approved"),
            (u"3", "rejected")
        ]
        return form


class BenefitAdmin(admin.ModelAdmin):

    list_display = ["name", "type", "description"]
    inlines = [BenefitLevelInline]


class SponsorLevelAdmin(admin.ModelAdmin):

    inlines = [BenefitLevelInline]


admin.site.register(SponsorLevel, SponsorLevelAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Benefit, BenefitAdmin)
