from django.conf.urls.defaults import *


urlpatterns = patterns("symposion.proposals.views",
    url(r"^submit/$", "proposal_submit", name="proposal_submit"),
    url(r"^submit/(\w+)/$", "proposal_submit_kind", name="proposal_submit_kind"),
    url(r"^(\d+)/$", "proposal_detail", name="proposal_detail"),
    url(r"^(\d+)/edit/$", "proposal_edit", name="proposal_edit"),
    url(r"^(\d+)/speakers/$", "proposal_speaker_manage", name="proposal_speaker_manage"),
    url(r"^(\d+)/cancel/$", "proposal_cancel", name="proposal_cancel"),
    url(r"^(\d+)/leave/$", "proposal_leave", name="proposal_leave"),
    url(r"^(\d+)/join/$", "proposal_pending_join", name="proposal_pending_join"),
    url(r"^(\d+)/decline/$", "proposal_pending_decline", name="proposal_pending_decline"),
    
    url(r"^(\d+)/document/create/$", "document_create", name="proposal_document_create"),
    url(r"^document/(\d+)/delete/$", "document_delete", name="proposal_document_delete"),
    url(r"^document/(\d+)/([^/]+)$", "document_download", name="proposal_document_download"),
)
