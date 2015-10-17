from django.db.models.signals import post_save
from django.dispatch import receiver

from pinax.submissions.models import SubmissionResult

from .models import Presentation


def unpromote_proposal(proposal):
    if hasattr(proposal, "presentation") and proposal.presentation:
        proposal.presentation.delete()


def promote_proposal(proposal):
    if hasattr(proposal, "presentation") and proposal.presentation:
        # already promoted
        presentation = proposal.presentation
    else:
        presentation = Presentation.objects.create(
            title=proposal.title,
            description=proposal.description,
            abstract=proposal.abstract,
            speaker=proposal.speaker,
            section=proposal.section,
            proposal_base=proposal,
        )
        for speaker in proposal.additional_speakers.all():
            presentation.additional_speakers.add(speaker)
            presentation.save()
    return presentation


@receiver(post_save, sender=SubmissionResult)
def handle_submissionresult_save(sender, instance, **kwargs):
    if instance.accepted:
        promote_proposal(instance.submission)
    else:
        unpromote_proposal(instance.submission)
