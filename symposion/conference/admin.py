from django.contrib import admin

from symposion.conference.models import PresentationKind, PresentationCategory


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class KindAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(PresentationCategory, CategoryAdmin)
admin.site.register(PresentationKind, KindAdmin)
