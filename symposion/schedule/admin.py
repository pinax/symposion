from django.contrib import admin

from schedule.models import SessionRole, Presentation, Slot, Session, Track


admin.site.register(Session)
admin.site.register(SessionRole,
    list_display = ["session", "user", "role", "status", "submitted"],
    raw_id_fields = ["user"],
)

admin.site.register(Track,
    list_display = ["pk", "name"]
)

admin.site.register(Slot,
    list_display = ["pk", "start", "end", "track"]
)

admin.site.register(Presentation,
    list_display = ["title", "slot", "presentation_type", "audience_level", "cancelled"],
    raw_id_fields = ["speaker"]
)