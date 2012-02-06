from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from cms.models import MenuItem, Page


class PageAdmin(MPTTModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "published", "status")

admin.site.register(Page, PageAdmin)


class MenuItemAdmin(MPTTModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "login_required", "published",)

admin.site.register(MenuItem, MenuItemAdmin)
