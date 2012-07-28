from django.contrib import admin

import reversion

from symposion.teams.models import Team, Membership

admin.site.register(Team,
    prepopulated_fields={"slug": ("name",)},
)


class MembershipAdmin(reversion.VersionAdmin):
    list_display = ["team", "user", "state"]
    list_filter = ["team"]
    search_fields = ["user__username"]

admin.site.register(Membership, MembershipAdmin)
