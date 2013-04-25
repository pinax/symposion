from django import template

from symposion.reviews.models import Review, ReviewAssignment
from symposion.proposals.models import ProposalBase


register = template.Library()


@register.assignment_tag(takes_context=True)
def user_reviews(context):
    request = context["request"]
    reviews = Review.objects.filter(user=request.user)
    return reviews

@register.assignment_tag(takes_context=True)
def user_not_reviewed(context):
	request = context["request"]
	already_reviewed = [r.proposal_id for r in Review.objects.filter(user=request.user)]
	yet_to_review = ProposalBase.objects.exclude(id__in=[p.id for p in ProposalBase.objects.filter(id__in=already_reviewed)]).exclude(speaker=request.user)
	return yet_to_review

@register.assignment_tag(takes_context=True)
def review_assignments(context):
    request = context["request"]
    assignments = ReviewAssignment.objects.filter(user=request.user)
    return assignments
