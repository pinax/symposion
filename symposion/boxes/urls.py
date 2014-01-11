from django.conf.urls import url, patterns


urlpatterns = patterns("symposion.boxes.views",
    url(r"^([-\w]+)/edit/$", "box_edit", name="box_edit"),
)
