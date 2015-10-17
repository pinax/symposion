from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    url(r"^users/$", views.user_list, name="user_list"),
)
