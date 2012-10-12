from django.conf.urls.defaults import *


urlpatterns = patterns("symposion.conference.views",
    url(r"^users/$", "user_list", name="user_list"),
)
