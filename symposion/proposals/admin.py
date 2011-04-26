from django.contrib import admin

from proposals.models import Proposal, ProposalSessionType


admin.site.register(ProposalSessionType)
admin.site.register(Proposal,
    list_display = ["title", "session_type", "audience_level", "cancelled", "extreme_pycon", "invited"]
)