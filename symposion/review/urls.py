from django.conf.urls.defaults import patterns, url, include, handler404, handler500


urlpatterns = patterns("review.views",
    url(r"^list/$", "review_list", name="review_list"),
    url(r"^list/(?P<username>[\w\-]+)/$", "review_list", name="review_list_user"),
    url(r"^tutorial/list/$", "review_tutorial_list", name="review_tutorial_list"),
    url(r"^tutorial/list/(?P<username>[\w\-]+)/$", "review_tutorial_list", name="review_tutorial_list_user"),
    url(r"^admin/$", "review_admin", name="review_admin"),
    url(r"^stats/$", "review_stats", name="review_stats"),
    url(r"^stats/(?P<key>[\w]+)/$", "review_stats", name="review_stats_key"),
    url(r"^(?P<pk>\d+)/$", "review_detail", name="review_detail"),
    url(r"^(?P<pk>\d+)/delete/$", "review_delete", name="review_delete"),
    url(r"^assignments/$", "review_assignments", name="review_assignments"),
    url(r"^assignment/(?P<pk>\d+)/opt-out/$", "review_assignment_opt_out", name="review_assignment_opt_out"),
)
