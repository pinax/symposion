from django.conf.urls import patterns, url


urlpatterns = patterns(
    "symposion.boxes.views",
    url(r"^([-\w]+)/edit/$", "box_edit", name="box_edit"),
)
