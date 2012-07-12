from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("pycon.sponsorship.views",
    url(r"^$", direct_to_template, {"template": "sponsorship/list.html"}, name="sponsor_list"),
    # url(r"^jobs/$", direct_to_template, {"template": "sponsors/jobs.html"}, name="sponsor_jobs"),
    url(r"^apply/$", "sponsor_apply", name="sponsor_apply"),
    url(r"^(?P<pk>\d+)/$", "sponsor_detail", name="sponsor_detail"),
)
