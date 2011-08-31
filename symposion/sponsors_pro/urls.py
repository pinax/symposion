from django.conf.urls.defaults import patterns, url, include, handler404, handler500
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("symposion.sponsors_pro.views",
    url(r"^$", direct_to_template, {"template": "sponsors/list.html"}, name="sponsor_list"),
    url(r"^info/$", "sponsor_info", name="sponsor_info"),
    url(r"^jobs/$", direct_to_template, {"template": "sponsors/jobs.html"}, name="sponsor_jobs"),
    url(r"^apply/$", "sponsor_apply", name="sponsor_apply"),
    url(r"^terms/$", direct_to_template, {"template": "sponsors/terms.html"}, name="sponsor_terms"),
    url(r"^(?P<pk>\d+)/$", "sponsor_detail", name="sponsor_detail"),
)
