from django.conf.urls.defaults import url, patterns


urlpatterns = patterns("symposion.schedule.views",
    url(r"^$", "schedule_detail", name="schedule_detail_slugless"),
    url(r"^edit/$", "schedule_edit", name="schedule_edit_slugless"),
    url(r"^list/$", "schedule_list", name="schedule_list_slugless"),
    url(r"^(\w+)/$", "schedule_detail", name="schedule_detail"),
    url(r"^(\w+)/edit/$", "schedule_edit", name="schedule_edit"),
    url(r"^(\w+)/list/$", "schedule_list", name="schedule_list"),
    url(r"^(\w+)/edit/slot/(\d+)/", "schedule_slot_edit", name="schedule_slot_edit"),
)
