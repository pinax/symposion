from django.contrib import admin

from symposion.schedule.models import SessionRole, Presentation, Slot, Session, Track


admin.site.register(Session)
admin.site.register(SessionRole,
    list_display = ["session", "user", "role", "status", "submitted"],
    raw_id_fields = ["user"],
)

admin.site.register(Track,
    list_display = ["pk", "name"]
)

admin.site.register(Slot,
    list_display = ["pk", "title", "start", "end", "track"]
)

admin.site.register(Presentation,
    list_display = [
        "pk",
        "title",
        "slot",
        "kind",
        "audience_level",
        "cancelled"
    ],
    list_filter = [
        "kind",
        "cancelled",
    ],
    raw_id_fields = ["speaker"]
)