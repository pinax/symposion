from django.conf.urls.defaults import patterns, url, include, handler404, handler500
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("schedule.views",
    # url(r"^$", "schedule_list", name="schedule_list"),
    # url(r"^presentations/(\d+)/", "schedule_presentation", name="schedule_presentation"),
    
    url(r"^index/$", direct_to_template, {"template": "schedule/index.html"}, name="schedule_index"),
    
    url(r"^lists/talks/", "schedule_list_talks", name="schedule_list_talks"),
    url(r"^lists/tutorials/", "schedule_list_tutorials", name="schedule_list_tutorials"),
    url(r"^lists/posters/", "schedule_list_posters", name="schedule_list_posters"),
    
    url(r"^tutorials/", "schedule_tutorials", name="schedule_tutorials"),
    url(r"^conference/edit/$", "schedule_conference_edit", name="schedule_conference_edit"),
    url(r"^$", "schedule_conference", name="schedule_conference"),
    url(r"^presentations/(\d+)/", "schedule_presentation", name="schedule_presentation"),
    
    url(r"slot/(\d+)/edit/$", "schedule_slot_edit", name="schedule_slot_edit"),
    url(r"slot/(\d+)/remove/$", "schedule_slot_remove", name="schedule_slot_remove"),
    url(r"^slot/(\d+)/(\w+)/$", "schedule_slot_add", name="schedule_slot_add"),
    url(r"^user_slot/(\d+)/$", "schedule_user_slot_manage", name="schedule_user_slot_manage"),
    
    url(r"^tracks/$", "track_list", name="schedule_track_list"),
    url(r"^sessions/$", "session_list", name="schedule_session_list"),
    url(r"^track/(\d+)/$", "track_detail", name="schedule_track_detail"),
    url(r"^track/none/$", "track_detail_none", name="schedule_notrack_detail"),
    url(r"^session/(\d+)/$", "session_detail", name="schedule_session_detail"),
    
    url(r"^bookmarks/(\d+)/(\w+)/$", "schedule_user_bookmarks", name="schedule_user_bookmarks"),
)