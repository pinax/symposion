from django.conf.urls.defaults import *


urlpatterns = patterns("proposals.views",
    url(r"^submit/$", "proposal_submit", name="proposal_submit"),
    url(r"^(\d+)/$", "proposal_detail", name="proposal_detail"),
    url(r"^(\d+)/edit/$", "proposal_edit", name="proposal_edit"),
    url(r"^(\d+)/speakers/$", "proposal_speaker_manage", name="proposal_speaker_manage"),
    url(r"^(\d+)/cancel/$", "proposal_cancel", name="proposal_cancel"),
    url(r"^(\d+)/leave/$", "proposal_leave", name="proposal_leave"),
)
