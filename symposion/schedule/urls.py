from django.conf.urls.defaults import url, patterns


urlpatterns = patterns("symposion.schedule.views",
    url(r"^$", "schedule_detail", name="schedule_detail_singleton"),
    url(r"^edit/$", "schedule_edit", name="schedule_edit_singleton"),
    url(r"^(\w+)/edit/$", "schedule_detail", name="schedule_detail"),
    url(r"^(\w+)/edit/$", "schedule_edit", name="schedule_edit"),
    url(r"^edit/slot/(?P<slot_pk>\d+)/", "schedule_slot_edit", name="schedule_slot_edit"),
    url(r"^list/$", "schedule_list", name="schedule_list"),
)
