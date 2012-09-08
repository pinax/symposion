from django.conf.urls.defaults import patterns, url


urlpatterns = patterns("symposion.reviews.views",
    url(r"^section/(?P<section_slug>[\w\-]+)/$", "review_section", name="review_section"),
    url(r"^section/(?P<section_slug>[\w\-]+)/assignments/$", "review_section", {"assigned": True}, name="review_section_assignments"),
    url(r"^section/(?P<section_slug>[\w\-]+)/status/$", "review_status", name="review_status"),
    url(r"^section/(?P<section_slug>[\w\-]+)/status/(?P<key>\w+)/$", "review_status", name="review_status"),
    url(r"^section/(?P<section_slug>[\w\-]+)/list/(?P<user_pk>\d+)/$", "review_list", name="review_list_user"),
    url(r"^section/(?P<section_slug>[\w\-]+)/admin/$", "review_admin", name="review_admin"),
    url(r"^section/(?P<section_slug>[\w\-]+)/admin/accept/$", "review_bulk_accept", name="review_bulk_accept"),
    url(r"^section/(?P<section_slug>[\w\-]+)/notification/(?P<status>\w+)/$", "result_notification", name="result_notification"),
    url(r"^section/(?P<section_slug>[\w\-]+)/notification/(?P<status>\w+)/prepare/$", "result_notification_prepare", name="result_notification_prepare"),
    url(r"^section/(?P<section_slug>[\w\-]+)/notification/(?P<status>\w+)/send/$", "result_notification_send", name="result_notification_send"),
    
    url(r"^review/(?P<pk>\d+)/$", "review_detail", name="review_detail"),
    
    url(r"^(?P<pk>\d+)/delete/$", "review_delete", name="review_delete"),
    url(r"^assignments/$", "review_assignments", name="review_assignments"),
    url(r"^assignment/(?P<pk>\d+)/opt-out/$", "review_assignment_opt_out", name="review_assignment_opt_out"),
)
