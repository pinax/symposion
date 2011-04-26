from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from pinax.apps.account.forms import LoginForm

from proposals.models import Proposal
from speakers.forms import SpeakerForm, SignupForm
from speakers.models import Speaker


def speaker_dashboard(request):
    ctx = {}
    if request.user.is_authenticated():
        if Speaker.objects.filter(user=request.user).exists():
            proposals = Proposal.objects.filter(
                Q(speaker=request.user.speaker_profile) |
                Q(additional_speakers=request.user.speaker_profile)
            ).distinct()
            if proposals.count():
                ctx["proposal_text"] = "submit another talk proposal"
            else:
                ctx["proposal_text"] = "submit a talk proposal"
            ctx["proposals"] = proposals
            template_name = "dashboard_auth_speaker.html"
        else:
            template_name = "dashboard_auth_nospeaker.html"
    else:
        template_name = "dashboard_noauth.html"
    ctx["accepting_proposals"] = settings.ACCEPTING_PROPOSALS
    ctx = RequestContext(request, ctx)
    return render_to_response("speakers/%s" % template_name, ctx)


@login_required
def speaker_create(request):
    try:
        return redirect(request.user.speaker_profile)
    except ObjectDoesNotExist:
        pass
    if request.method == "POST":
        try:
            speaker = Speaker.objects.get(invite_email=request.user.email)
            found = True
        except Speaker.DoesNotExist:
            speaker = None
            found = False
        form = SpeakerForm(request.POST, request.FILES, instance=speaker)
        if form.is_valid():
            speaker = form.save(commit=False)
            speaker.user = request.user
            if not found:
                speaker.invite_email = None
            speaker.save()
            messages.success(request, "Speaker profile created.")
            return redirect("speaker_dashboard")
    else:
        form = SpeakerForm()
    ctx = {
        "form": form,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("speakers/speaker_create.html", ctx)


def speaker_create_token(request, token):
    speaker = get_object_or_404(Speaker, invite_token=token)
    if request.user.is_authenticated():
        # check for speaker profile
        try:
            existing_speaker = request.user.speaker_profile
        except ObjectDoesNotExist:
            pass
        else:
            additional_speakers = Proposal.additional_speakers.through
            additional_speakers._default_manager.filter(
                speaker = speaker
            ).update(
                speaker = existing_speaker
            )
            messages.info(request, "You have been associated with all pending "
                "talk proposals")
            return redirect("speaker_dashboard")
    if request.method == "POST":
        if "login" in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                login_form.login(request)
                return redirect("speaker_create_token", token)
            else:
                signup_form = SignupForm(initial={"email": speaker.invite_email}, prefix="signup")
                speaker_form = None
        elif "signup" in request.POST:
            login_form = None
            forms = []
            if not request.user.is_authenticated():
                login_form = None
                signup_form = SignupForm(request.POST, prefix="signup")
                forms.append(signup_form)
            speaker_form = SpeakerForm(request.POST, request.FILES,
                prefix = "speaker",
                instance = speaker
            )
            forms.append(speaker_form)
            if all([f.is_valid() for f in forms]):
                if not request.user.is_authenticated():
                    user = signup_form.save(speaker, request=request)
                else:
                    user = request.user
                speaker = speaker_form.save(commit=False)
                speaker.user = user
                speaker.save()
                if not request.user.is_authenticated():
                    if user.email != speaker.invite_email:
                        ctx = {
                            "email": user.email,
                            "success_url": "/",
                        }
                        ctx = RequestContext(request, ctx)
                        return render_to_response("account/verification_sent.html", ctx)
                    else:
                        signup_form.login(request, user)
                return redirect("speaker_dashboard")
        else:
            raise Exception("wtf?")
    else:
        if not request.user.is_authenticated():
            login_form = LoginForm()
            signup_form = SignupForm(initial={"email": speaker.invite_email}, prefix="signup")
        else:
            login_form, signup_form = None, None
        speaker_form = SpeakerForm(prefix="speaker")
    ctx = {
        "login_form": login_form,
        "signup_form": signup_form,
        "speaker_form": speaker_form,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("speakers/speaker_create_token.html", ctx)


@login_required
def speaker_edit(request, pk=None):
    if pk is None:
        try:
            speaker = request.user.speaker_profile
        except Speaker.DoesNotExist:
            return redirect("speaker_create")
    else:
        if request.user.groups.filter(name="organizer").exists():
            speaker = get_object_or_404(Speaker, pk=pk)
        else:
            raise Http404()
    if request.method == "POST":
        form = SpeakerForm(request.POST, request.FILES, instance=speaker)
        if form.is_valid():
            form.save()
            messages.success(request, "Speaker profile updated.")
            return redirect("speaker_dashboard")
    else:
        form = SpeakerForm(instance=speaker)
    ctx = {
        "form": form,
    }
    ctx = RequestContext(request, ctx)
    return render_to_response("speakers/speaker_edit.html", ctx)


def speaker_profile(request, pk, template_name="speakers/speaker_profile.html", extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    
    speaker = get_object_or_404(Speaker, pk=pk)
    
    return render_to_response(template_name, dict({
        "speaker": speaker,
        "sessions": speaker.sessions.exclude(slot=None).order_by("slot__start"),
        "timezone": settings.SCHEDULE_TIMEZONE,
    }, **extra_context), context_instance=RequestContext(request))
