from django.contrib import admin

from symposion.schedule.models import Schedule, Day, Room, SlotKind, Slot, SlotRoom, Presentation, Session, SessionRole


admin.site.register(Schedule)
admin.site.register(Day)
admin.site.register(
    Room,
    list_display=("name", "order", "schedule"),
    list_filter=("schedule",)
)
admin.site.register(
    SlotKind,
    list_display=("label", "schedule"),
)
admin.site.register(
    Slot,
    list_display=("day", "start", "end", "kind", "content")
)
admin.site.register(
    SlotRoom,
    list_display=("slot", "room")
)
admin.site.register(Session)
admin.site.register(SessionRole)
admin.site.register(
    Presentation,
    list_filter=("section", "cancelled", "slot")
)
