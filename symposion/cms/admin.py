from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from cms.models import Page


class PageAdmin(MPTTModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "published", "status")

admin.site.register(Page, PageAdmin)
