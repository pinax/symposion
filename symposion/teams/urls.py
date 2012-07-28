from django.conf.urls.defaults import *


urlpatterns = patterns("symposion.teams.views",
    url(r"^(\w+)/$", "team_detail", name="team_detail"),
)
