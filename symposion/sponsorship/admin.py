from django.contrib import admin
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from symposion.sponsorship.models import SponsorLevel, Sponsor, Benefit, BenefitLevel, \
    SponsorBenefit


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


class SponsorAdmin(admin.ModelAdmin):

    save_on_top = True
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
    list_display = ["name", "external_url", "level", "active", "contact", "applicant_field"]

    def contact(self, sponsor):
        return mark_safe('<a href="mailto:%s">%s</a>' % (escape(sponsor.contact_email), escape(sponsor.contact_name)))

    def applicant_field(self, sponsor):
        name = sponsor.applicant.get_full_name()
        email = sponsor.applicant.email
        return mark_safe('<a href="mailto:%s">%s</a>' % (escape(email), escape(name)))
    applicant_field.short_description = _(u"Applicant")

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
