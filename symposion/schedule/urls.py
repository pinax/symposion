from django.conf.urls.defaults import url, patterns


urlpatterns = patterns("symposion.schedule.views",
    url(r"^$", "schedule_detail", name="schedule_detail"),
    url(r"^edit/$", "schedule_edit", name="schedule_edit"),
    url(r"^list/$", "schedule_list", name="schedule_list"),
    url(r"^presentations.csv$", "schedule_list_csv", name="schedule_list_csv"),
    url(r"^presentation/(\d+)/$", "schedule_presentation_detail", name="schedule_presentation_detail"),
    url(r"^(\w+)/$", "schedule_detail", name="schedule_detail"),
    url(r"^(\w+)/edit/$", "schedule_edit", name="schedule_edit"),
    url(r"^(\w+)/list/$", "schedule_list", name="schedule_list"),
    url(r"^(\w+)/presentations.csv$", "schedule_list_csv", name="schedule_list_csv"),
    url(r"^(\w+)/edit/slot/(\d+)/", "schedule_slot_edit", name="schedule_slot_edit"),
)
