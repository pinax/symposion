from django.contrib.contenttypes.models import ContentType

from symposion.proposals.models import ProposalSection


def reviews(request):
    kinds = []
    for proposal_section in ProposalSection.available():
        for kind in proposal_section.section.proposal_kinds.all():
            kinds.append(kind)
    # @@@ need to check perms here and include in context
    return {
        "review_kinds": kinds,
    }
