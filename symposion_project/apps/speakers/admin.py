from django.contrib import admin

from . import models


admin.site.register(models.Speaker,
    list_display=("user",))
