from django.conf import settings
from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

import symposion.views

# from pinax.apps.account.openid_consumer import PinaxConsumer

WIKI_SLUG = r"(([\w-]{2,})(/[\w-]{2,})*)"

urlpatterns = patterns("",
    (r'^i18n/', include('django.conf.urls.i18n')),
)

urlpatterns += i18n_patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),

    url(r"^sponsors/prospectus/$", direct_to_template, {
        "template": "sponsor_prospectus.html",
    }, name="sponsor_prospectus"),

    url(r"^about/", direct_to_template, {
        "template": "about.html",
    }, name="about"),

    url(r"^venue/", direct_to_template, {
        "template": "venue.html",
    }, name="venue"),

    url(r"^speak/", direct_to_template, {
        "template": "speak.html",
    }, name="speak"),

    url(r"^learn/", direct_to_template, {
        "template": "learn.html",
    }, name="learn"),

    url(r"^contact/", direct_to_template, {
        "template": "contact.html",
    }, name="contact"),

    url(r"^conduct/", direct_to_template, {
        "template": "conduct.html",
    }, name="conduct"),

    url(r"^admin/", include(admin.site.urls)),

    url(r"^account/signup/$", symposion.views.SignupView.as_view(), name="account_signup"),
    url(r"^account/login/$", symposion.views.LoginView.as_view(), name="account_login"),
    url(r"^account/", include("account.urls")),

    url(r"^dashboard/", symposion.views.dashboard, name="dashboard"),
    url(r"^speaker/", include("symposion.speakers.urls")),
    url(r"^proposals/", include("symposion.proposals.urls")),
    url(r"^sponsors/", include("symposion.sponsorship.urls")),
    url(r"^boxes/", include("symposion.boxes.urls")),
    url(r"^teams/", include("symposion.teams.urls")),
    url(r"^reviews/", include("symposion.reviews.urls")),
    url(r"^schedule/", include("symposion.schedule.urls")),
    url(r"^markitup/", include("markitup.urls")),
)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
