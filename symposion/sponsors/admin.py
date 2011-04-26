from django.contrib import admin

from sponsors.models import SponsorLevel, Sponsor, Benefit, BenefitLevel, SponsorBenefit


class BenefitLevelInline(admin.TabularInline):
    model = BenefitLevel
    extra = 0


class SponsorBenefitInline(admin.StackedInline):
    model = SponsorBenefit
    extra = 0

    fieldsets = [(None, {'fields': [('benefit', 'active'),
                                    ('max_words', 'other_limits'),
                                    'text', 'upload']})]


class SponsorAdmin(admin.ModelAdmin):
    def get_form(self, *args, **kwargs):
        # @@@ kinda ugly but using choices= on NullBooleanField is broken
        form = super(SponsorAdmin, self).get_form(*args, **kwargs)
        form.base_fields['active'].widget.choices = [(u'1', "unreviewed"),
                                                     (u'2', "approved"),
                                                     (u'3', "rejected")]
        return form

    save_on_top = True

    fieldsets = [(None, {'fields': [('name', 'applicant'),
                                    ('level', 'active'),
                                    'external_url', 'annotation',
                                    ('contact_name', 'contact_email')]}),
                 ('Metadata', {'fields': ['added'],
                               'classes': ['collapse']})]
    
    inlines = [SponsorBenefitInline]


class BenefitAdmin(admin.ModelAdmin):
    inlines = [BenefitLevelInline]


class SponsorLevelAdmin(admin.ModelAdmin):
    inlines = [BenefitLevelInline]
    
admin.site.register(SponsorLevel, SponsorLevelAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Benefit, BenefitAdmin)
