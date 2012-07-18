from django.contrib import admin

import reversion

from .models import Page

class PageAdmin(reversion.VersionAdmin):

    pass


admin.site.register(Page, PageAdmin)
