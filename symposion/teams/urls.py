from django.conf.urls.defaults import *


urlpatterns = patterns("symposion.teams.views",
    url(r"^(?P<slug>[\w\-]+)/$", "team_detail", name="team_detail"),
    url(r"^(?P<slug>[\w\-]+)/join/$", "team_join", name="team_join"),
    url(r"^(?P<slug>[\w\-]+)/leave/$", "team_leave", name="team_leave"),
    url(r"^(?P<slug>[\w\-]+)/apply/$", "team_apply", name="team_apply"),
    
    url(r"^promote/(?P<pk>\d+)/$", "team_promote", name="team_promote"),
    url(r"^demote/(?P<pk>\d+)/$", "team_demote", name="team_demote"),
)
