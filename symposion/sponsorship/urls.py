from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns(
    "symposion.sponsorship.views",
    url(r"^$", TemplateView.as_view(template_name="sponsorship/list.html"), name="sponsor_list"),
    url(r"^apply/$", "sponsor_apply", name="sponsor_apply"),
    url(r"^add/$", "sponsor_add", name="sponsor_add"),
    url(r"^ziplogos/$", "sponsor_zip_logo_files", name="sponsor_zip_logos"),
    url(r"^(?P<pk>\d+)/$", "sponsor_detail", name="sponsor_detail"),
)
