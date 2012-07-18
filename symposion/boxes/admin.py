from django.contrib import admin

import reversion

from symposion.boxes.models import Box


class BoxAdmin(reversion.VersionAdmin):

    pass

admin.site.register(Box, BoxAdmin)
