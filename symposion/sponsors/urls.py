from django.conf.urls.defaults import patterns, url, include, handler404, handler500


urlpatterns = patterns("sponsors.views",
    url(r"^$", "sponsor_index", name="sponsor_index"),
    url(r"^apply/$", "sponsor_apply", name="sponsor_apply"),
    url(r"^(?P<pk>\d+)/$", "sponsor_detail", name="sponsor_detail"),
)
