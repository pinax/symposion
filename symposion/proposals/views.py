import random

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.hashcompat import sha_constructor
from django.utils.html import strip_tags

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from emailconfirmation.models import EmailAddress

from symposion.proposals.forms import ProposalSubmitForm, ProposalEditForm, AddSpeakerForm
from symposion.proposals.models import Proposal
from symposion.speakers.models import Speaker
from symposion.utils.mail import send_email


def proposal_submit(request):
    if not request.user.is_authenticated():
        return redirect("speaker_dashboard")
    else:
        try:
            speaker_profile = request.user.speaker_profile
        except ObjectDoesNotExist:
            return redirect("speaker_dashboard")
    if not settings.ACCEPTING_PROPOSALS:
        return redirect("speaker_dashboard")
    if request.method == "POST":
        form = ProposalSubmitForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.speaker = speaker_profile
            proposal.save()
            form.save_m2m()
            messages.success(request, "Talk proposal submitted.")
            if "add-speakers" in request.POST:
                return redirect("proposal_speaker_manage", proposal.pk)
            return redirect("speaker_dashboard")
    else:
        form = ProposalSubmitForm()
    ctx = {
        "form": form,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("proposals/proposal_submit.html", ctx)


@login_required
def proposal_speaker_manage(request, pk):
    queryset = Proposal.objects.select_related("speaker")
    proposal = get_object_or_404(queryset, pk=pk)
    if proposal.speaker != request.user.speaker_profile:
        raise Http404()
    if request.method == "POST":
        add_speaker_form = AddSpeakerForm(request.POST, proposal=proposal)
        if add_speaker_form.is_valid():
            message_ctx = {
                "proposal": proposal,
            }
            def create_speaker_token(email_address):
                # create token and look for an existing speaker to prevent
                # duplicate tokens and confusing the pending speaker
                try:
                    pending = Speaker.objects.get(
                        Q(user=None, invite_email=email_address)
                    )
                except Speaker.DoesNotExist:
                    salt = sha_constructor(str(random.random())).hexdigest()[:5]
                    token = sha_constructor(salt+email_address).hexdigest()
                    pending = Speaker.objects.create(
                        invite_email = email_address,
                        invite_token = token,
                    )
                else:
                    token = pending.invite_token
                return pending, token
            email_address = add_speaker_form.cleaned_data["email"]
            # check if email is on the site now
            users = EmailAddress.objects.get_users_for(email_address)
            if users:
                # should only be one since we enforce unique email
                user = users[0]
                message_ctx["user"] = user
                # look for speaker profile
                try:
                    speaker = user.speaker_profile
                except ObjectDoesNotExist:
                    speaker, token = create_speaker_token(email_address)
                    message_ctx["token"] = token
                    # fire off email to user to create profile
                    send_email(
                        [email_address], "speaker_no_profile",
                        context = message_ctx
                    )
                else:
                    # fire off email to user letting them they are loved.
                    send_email(
                        [email_address], "speaker_addition",
                        context = message_ctx
                    )
            else:
                speaker, token = create_speaker_token(email_address)
                message_ctx["token"] = token
                # fire off email letting user know about site and to create
                # account and speaker profile
                send_email(
                    [email_address], "speaker_invite",
                    context = message_ctx
                )
            proposal.additional_speakers.add(speaker)
            messages.success(request, "Speaker added to proposal.")
            return redirect("proposal_speaker_manage", proposal.pk)
    else:
        add_speaker_form = AddSpeakerForm(proposal=proposal)
    ctx = {
        "proposal": proposal,
        "speakers": proposal.speakers(),
        "add_speaker_form": add_speaker_form,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("proposals/proposal_speaker_manage.html", ctx)


@login_required
def proposal_edit(request, pk):
    queryset = Proposal.objects.select_related("speaker")
    proposal = get_object_or_404(queryset, pk=pk)
    if request.user != proposal.speaker.user:
        raise Http404()
    if not proposal.can_edit():
        ctx = RequestContext(request, {
            "title": "Proposal editing closed",
            "body": "Proposal editing is closed for this session type."
        })
        return render_to_response("proposals/proposal_error.html", ctx)
    if request.method == "POST":
        form = ProposalEditForm(request.POST, instance=proposal)
        if form.is_valid():
            form.save()
            messages.success(request, "Proposal updated.")
            return redirect("proposal_detail", proposal.pk)
    else:
        form = ProposalEditForm(instance=proposal)
    ctx = {
        "proposal": proposal,
        "form": form,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("proposals/proposal_edit.html", ctx)


@login_required
def proposal_detail(request, pk):
    queryset = Proposal.objects.select_related("speaker", "speaker__user")
    proposal = get_object_or_404(queryset, pk=pk)
    
    if request.user not in [p.user for p in proposal.speakers()]:
        raise Http404()
    
    from symposion.review.forms import SpeakerCommentForm
    message_form = SpeakerCommentForm()
    if request.method == "POST":
        message_form = SpeakerCommentForm(request.POST)
        if message_form.is_valid():
            
            message = message_form.save(commit=False)
            message.user = request.user
            message.proposal = proposal
            message.save()
            
            ProposalMessage = SpeakerCommentForm.Meta.model
            reviewers = User.objects.filter(
                id__in=ProposalMessage.objects.filter(
                    proposal=proposal
                ).exclude(
                    user=request.user
                ).distinct().values_list("user", flat=True)
            )
            
            for reviewer in reviewers:
                ctx = {
                    "proposal": proposal,
                    "message": message,
                    "reviewer": True,
                }
                send_email(
                    [reviewer.email], "proposal_new_message",
                    context = ctx
                )
            
            return redirect(request.path)
    else:
        message_form = SpeakerCommentForm()
    
    ctx = {
        "proposal": proposal,
        "message_form": message_form,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("proposals/proposal_detail.html", ctx)


@login_required
def proposal_cancel(request, pk):
    queryset = Proposal.objects.select_related("speaker")
    proposal = get_object_or_404(queryset, pk=pk)
    if proposal.speaker.user != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        proposal.cancelled = True
        proposal.save()
        # @@@ fire off email to submitter and other speakers
        messages.success(request, "%s has been cancelled" % proposal.title)
        return redirect("speaker_dashboard")
    ctx = {
        "proposal": proposal,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("proposals/proposal_cancel.html", ctx)


@login_required
def proposal_leave(request, pk):
    queryset = Proposal.objects.select_related("speaker")
    proposal = get_object_or_404(queryset, pk=pk)
    try:
        speaker = proposal.additional_speakers.get(user=request.user)
    except ObjectDoesNotExist:
        return HttpResponseForbidden()
    if request.method == "POST":
        proposal.additional_speakers.remove(speaker)
        # @@@ fire off email to submitter and other speakers
        messages.success(request, "You are no longer speaking on %s" % proposal.title)
        return redirect("speaker_dashboard")
    ctx = {
        "proposal": proposal,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("proposals/proposal_leave.html", ctx)
