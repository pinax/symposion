import re

from django.core.mail import send_mass_mail
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.template import Context, Template
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required

from symposion.conf import settings
from symposion.proposals.models import ProposalBase, ProposalSection
from symposion.teams.models import Team
from symposion.utils.mail import send_email

from symposion.reviews.forms import ReviewForm, SpeakerCommentForm
from symposion.reviews.forms import BulkPresentationForm
from symposion.reviews.models import (
    ReviewAssignment, Review, LatestVote, ProposalResult, NotificationTemplate,
    ResultNotification
)


def access_not_permitted(request):
    return render(request, "reviews/access_not_permitted.html")


def proposals_generator(request, queryset, user_pk=None, check_speaker=True):
    
    for obj in queryset:
        # @@@ this sucks; we can do better
        if check_speaker:
            if request.user in [s.user for s in obj.speakers()]:
                continue
        
        try:
            obj.result
        except ProposalResult.DoesNotExist:
            ProposalResult.objects.get_or_create(proposal=obj)
        
        obj.comment_count = obj.result.comment_count
        obj.total_votes = obj.result.vote_count
        obj.plus_one = obj.result.plus_one
        obj.plus_zero = obj.result.plus_zero
        obj.minus_zero = obj.result.minus_zero
        obj.minus_one = obj.result.minus_one
        lookup_params = dict(proposal=obj)
        
        if user_pk:
            lookup_params["user__pk"] = user_pk
        else:
            lookup_params["user"] = request.user
        
        try:
            obj.user_vote = LatestVote.objects.get(**lookup_params).vote
            obj.user_vote_css = LatestVote.objects.get(**lookup_params).css_class()
        except LatestVote.DoesNotExist:
            obj.user_vote = None
            obj.user_vote_css = "no-vote"
        
        yield obj


@login_required
def review_section(request, section_slug, assigned=False):
    
    if not request.user.has_perm("reviews.can_review_%s" % section_slug):
        return access_not_permitted(request)
    
    section = get_object_or_404(ProposalSection, section__slug=section_slug)
    queryset = ProposalBase.objects.filter(kind__section=section)
    
    if assigned:
        assignments = ReviewAssignment.objects.filter(user=request.user).values_list("proposal__id")
        queryset = queryset.filter(id__in=assignments)
    
    queryset = queryset.select_related("result").select_subclasses()
    
    proposals = proposals_generator(request, queryset)
    
    ctx = {
        "proposals": proposals,
        "section": section,
    }
    
    return render(request, "reviews/review_list.html", ctx)


@login_required
def review_list(request, section_slug, user_pk):
    
    # if they're not a reviewer admin and they aren't the person whose
    # review list is being asked for, don't let them in
    if not request.user.has_perm("reviews.can_manage_%s" % section_slug):
        if not request.user.pk == user_pk:
            return access_not_permitted(request)
    
    queryset = ProposalBase.objects.select_related("speaker__user", "result")
    reviewed = LatestVote.objects.filter(user__pk=user_pk).values_list("proposal", flat=True)
    queryset = queryset.filter(pk__in=reviewed)
    proposals = queryset.order_by("submitted")
    
    admin = request.user.has_perm("reviews.can_manage_%s" % section_slug)
    
    proposals = proposals_generator(request, proposals, user_pk=user_pk, check_speaker=not admin)
    
    ctx = {
        "proposals": proposals,
    }
    return render(request, "reviews/review_list.html", ctx)


@login_required
def review_admin(request, section_slug):
    
    if not request.user.has_perm("reviews.can_manage_%s" % section_slug):
        return access_not_permitted(request)
    
    def reviewers():
        already_seen = set()
        
        for team in Team.objects.filter(permissions__codename="can_review_%s" % section_slug):
            for membership in team.memberships.filter(Q(state="member") | Q(state="manager")):
                user = membership.user
                if user.pk in already_seen:
                    continue
                already_seen.add(user.pk)
                
                user.comment_count = Review.objects.filter(user=user).count()
                user.total_votes = LatestVote.objects.filter(user=user).count()
                user.plus_one = LatestVote.objects.filter(
                    user = user,
                    vote = LatestVote.VOTES.PLUS_ONE
                ).count()
                user.plus_zero = LatestVote.objects.filter(
                    user = user,
                    vote = LatestVote.VOTES.PLUS_ZERO
                ).count()
                user.minus_zero = LatestVote.objects.filter(
                    user = user,
                    vote = LatestVote.VOTES.MINUS_ZERO
                ).count()
                user.minus_one = LatestVote.objects.filter(
                    user = user,
                    vote = LatestVote.VOTES.MINUS_ONE
                ).count()
                
                yield user
    
    ctx = {
        "section_slug": section_slug,
        "reviewers": reviewers(),
    }
    return render(request, "reviews/review_admin.html", ctx)


@login_required
def review_detail(request, pk):
    
    proposals = ProposalBase.objects.select_related("result").select_subclasses()
    proposal = get_object_or_404(proposals, pk=pk)
    
    if not request.user.has_perm("reviews.can_review_%s" % proposal.kind.section.slug):
        return access_not_permitted(request)
    
    speakers = [s.user for s in proposal.speakers()]
    
    if not request.user.is_superuser and request.user in speakers:
        return access_not_permitted(request)
    
    admin = request.user.is_staff
    
    try:
        latest_vote = LatestVote.objects.get(proposal=proposal, user=request.user)
    except LatestVote.DoesNotExist:
        latest_vote = None
    
    if request.method == "POST":
        if request.user in speakers:
            return access_not_permitted(request)
        
        if "vote_submit" in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                
                review = review_form.save(commit=False)
                review.user = request.user
                review.proposal = proposal
                review.save()
                
                return redirect(request.path)
            else:
                message_form = SpeakerCommentForm()
        elif "message_submit" in request.POST:
            message_form = SpeakerCommentForm(request.POST)
            if message_form.is_valid():
                
                message = message_form.save(commit=False)
                message.user = request.user
                message.proposal = proposal
                message.save()
                
                for speaker in speakers:
                    if speaker and speaker.email:
                        ctx = {
                            "proposal": proposal,
                            "message": message,
                            "reviewer": False,
                        }
                        send_email(
                            [speaker.email], "proposal_new_message",
                            context = ctx
                        )
                
                return redirect(request.path)
            else:
                initial = {}
                if latest_vote:
                    initial["vote"] = latest_vote.vote
                if request.user in speakers:
                    review_form = None
                else:
                    review_form = ReviewForm(initial=initial)
        elif "result_submit" in request.POST:
            if admin:
                result = request.POST["result_submit"]
                
                if result == "accept":
                    proposal.result.status = "accepted"
                    proposal.result.save()
                elif result == "reject":
                    proposal.result.status = "rejected"
                    proposal.result.save()
                elif result == "undecide":
                    proposal.result.status = "undecided"
                    proposal.result.save()
                elif result == "standby":
                    proposal.result.status = "standby"
                    proposal.result.save()
            
            return redirect(request.path)
    else:
        initial = {}
        if latest_vote:
            initial["vote"] = latest_vote.vote
        if request.user in speakers:
            review_form = None
        else:
            review_form = ReviewForm(initial=initial)
        message_form = SpeakerCommentForm()
    
    proposal.comment_count = proposal.result.comment_count
    proposal.total_votes = proposal.result.vote_count
    proposal.plus_one = proposal.result.plus_one
    proposal.plus_zero = proposal.result.plus_zero
    proposal.minus_zero = proposal.result.minus_zero
    proposal.minus_one = proposal.result.minus_one
    
    reviews = Review.objects.filter(proposal=proposal).order_by("-submitted_at")
    messages = proposal.messages.order_by("submitted_at")
    
    return render(request, "reviews/review_detail.html", {
        "proposal": proposal,
        "latest_vote": latest_vote,
        "reviews": reviews,
        "review_messages": messages,
        "review_form": review_form,
        "message_form": message_form
    })


@login_required
@require_POST
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    section_slug = review.section.slug
    
    if not request.user.has_perm("reviews.can_manage_%s" % section_slug):
        return access_not_permitted(request)
    
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    
    return redirect("review_detail", pk=review.proposal.pk)


@login_required
def review_status(request, section_slug=None, key=None):
    
    if not request.user.has_perm("reviews.can_review_%s" % section_slug):
        return access_not_permitted(request)
    
    VOTE_THRESHOLD = settings.SYMPOSION_VOTE_THRESHOLD
    
    ctx = {
        "section_slug": section_slug,
        "vote_threshold": VOTE_THRESHOLD,
    }
    
    queryset = ProposalBase.objects.select_related("speaker__user", "result").select_subclasses()
    if section_slug:
        queryset = queryset.filter(kind__section__slug=section_slug)
    
    proposals = {
        # proposals with at least VOTE_THRESHOLD reviews and at least one +1 and no -1s, sorted by the 'score'
        "positive": queryset.filter(result__vote_count__gte=VOTE_THRESHOLD, result__plus_one__gt=0, result__minus_one=0).order_by("-result__score"),
        # proposals with at least VOTE_THRESHOLD reviews and at least one -1 and no +1s, reverse sorted by the 'score'
        "negative": queryset.filter(result__vote_count__gte=VOTE_THRESHOLD, result__minus_one__gt=0, result__plus_one=0).order_by("result__score"),
        # proposals with at least VOTE_THRESHOLD reviews and neither a +1 or a -1, sorted by total votes (lowest first)
        "indifferent": queryset.filter(result__vote_count__gte=VOTE_THRESHOLD, result__minus_one=0, result__plus_one=0).order_by("result__vote_count"),
        # proposals with at least VOTE_THRESHOLD reviews and both a +1 and -1, sorted by total votes (highest first)
        "controversial": queryset.filter(result__vote_count__gte=VOTE_THRESHOLD, result__plus_one__gt=0, result__minus_one__gt=0).order_by("-result__vote_count"),
        # proposals with fewer than VOTE_THRESHOLD reviews
        "too_few": queryset.filter(result__vote_count__lt=VOTE_THRESHOLD).order_by("result__vote_count"),
    }
    
    admin = request.user.has_perm("reviews.can_manage_%s" % section_slug)
    
    for status in proposals:
        if key and key != status:
            continue
        proposals[status] = list(proposals_generator(request, proposals[status], check_speaker=not admin))
    
    if key:
        ctx.update({
            "key": key,
            "proposals": proposals[key],
        })
    else:
        ctx["proposals"] = proposals
    
    return render(request, "reviews/review_stats.html", ctx)


@login_required
def review_assignments(request):
    if not request.user.groups.filter(name="reviewers").exists():
        return access_not_permitted(request)
    assignments = ReviewAssignment.objects.filter(
        user=request.user,
        opted_out=False
    )
    return render(request, "reviews/review_assignment.html", {
        "assignments": assignments,
    })


@login_required
@require_POST
def review_assignment_opt_out(request, pk):
    review_assignment = get_object_or_404(ReviewAssignment,
        pk=pk,
        user=request.user
    )
    if not review_assignment.opted_out:
        review_assignment.opted_out = True
        review_assignment.save()
        ReviewAssignment.create_assignments(review_assignment.proposal, origin=ReviewAssignment.AUTO_ASSIGNED_LATER)
    return redirect("review_assignments")


@login_required
def review_bulk_accept(request, section_slug):
    if not request.user.has_perm("reviews.can_manage_%s" % section_slug):
        return access_not_permitted(request)
    if request.method == "POST":
        form = BulkPresentationForm(request.POST)
        if form.is_valid():
            talk_ids = form.cleaned_data["talk_ids"].split(",")
            talks = ProposalBase.objects.filter(id__in=talk_ids).select_related("result")
            for talk in talks:
                talk.result.status = "accepted"
                talk.result.save()
            return redirect("review_list")
    else:
        form = BulkPresentationForm()
    
    return render(request, "reviews/review_bulk_accept.html", {
        "form": form,
    })


@login_required
def result_notification(request, section_slug, status):
    if not request.user.has_perm("reviews.can_manage_%s" % section_slug):
        return access_not_permitted(request)
    
    proposals = ProposalBase.objects.filter(kind__section__slug=section_slug, result__status=status).select_related("speaker__user", "result").select_subclasses()
    notification_templates = NotificationTemplate.objects.all()
    
    ctx = {
        "section_slug": section_slug,
        "status": status,
        "proposals": proposals,
        "notification_templates": notification_templates,
    }
    return render(request, "reviews/result_notification.html", ctx)


@login_required
def result_notification_prepare(request, section_slug, status):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    if not request.user.has_perm("reviews.can_manage_%s" % section_slug):
        return access_not_permitted(request)
    
    proposal_pks = []
    try:
        for pk in request.POST.getlist("_selected_action"):
            proposal_pks.append(int(pk))
    except ValueError:
        return HttpResponseBadRequest()
    proposals = ProposalBase.objects.filter(
        kind__section__slug=section_slug,
        result__status=status,
    )
    proposals = proposals.filter(pk__in=proposal_pks)
    proposals = proposals.select_related("speaker__user", "result")
    proposals = proposals.select_subclasses()
    
    notification_template_pk = request.POST.get("notification_template", "")
    if notification_template_pk:
        notification_template = NotificationTemplate.objects.get(pk=notification_template_pk)
    else:
        notification_template = None
    
    ctx = {
        "section_slug": section_slug,
        "status": status,
        "notification_template": notification_template,
        "proposals": proposals,
        "proposal_pks": ",".join([str(pk) for pk in proposal_pks]),
    }
    return render(request, "reviews/result_notification_prepare.html", ctx)


@login_required
def result_notification_send(request, section_slug, status):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    if not request.user.has_perm("reviews.can_manage_%s" % section_slug):
        return access_not_permitted(request)
    
    if not all([k in request.POST for k in ["proposal_pks", "from_address", "subject", "body"]]):
        return HttpResponseBadRequest()
    
    try:
        proposal_pks = [int(pk) for pk in request.POST["proposal_pks"].split(",")]
    except ValueError:
        return HttpResponseBadRequest()
    
    proposals = ProposalBase.objects.filter(
        kind__section__slug=section_slug,
        result__status=status,
    )
    proposals = proposals.filter(pk__in=proposal_pks)
    proposals = proposals.select_related("speaker__user", "result")
    proposals = proposals.select_subclasses()
    
    notification_template_pk = request.POST.get("notification_template", "")
    if notification_template_pk:
        notification_template = NotificationTemplate.objects.get(pk=notification_template_pk)
    else:
        notification_template = None
    
    emails = []
    
    for proposal in proposals:
        rn = ResultNotification()
        rn.proposal = proposal
        rn.template = notification_template
        rn.to_address = proposal.speaker_email
        rn.from_address = request.POST["from_address"]
        rn.subject = request.POST["subject"]
        rn.body = Template(request.POST["body"]).render(
            Context({
                "proposal": proposal.notification_email_context()
            })
        )
        rn.save()
        emails.append(rn.email_args)
    
    send_mass_mail(emails)
    
    return redirect("result_notification", section_slug=section_slug, status=status)
