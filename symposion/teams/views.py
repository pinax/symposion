from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from symposion.teams.forms import TeamInvitationForm
from symposion.teams.models import Team, Membership


## perm checks
#
# @@@ these can be moved

def can_join(team, user):
    state = team.get_state_for_user(user)
    if team.access == "open" and state is None:
        return True
    elif state == "invited":
        return True
    elif user.is_staff and state is None:
        return True
    else:
        return False


def can_leave(team, user):
    state = team.get_state_for_user(user)
    if state == "member":  # managers can't leave at the moment
        return True
    else:
        return False


def can_apply(team, user):
    state = team.get_state_for_user(user)
    if team.access == "application" and state is None:
        return True
    else:
        return False


def can_invite(team, user):
    state = team.get_state_for_user(user)
    if team.access == "invitation":
        if state == "manager" or user.is_staff:
            return True
    return False


## views


@login_required
def team_detail(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.get_state_for_user(request.user)
    if team.access == "invitation" and state is None and not request.user.is_staff:
        raise Http404()
    
    if can_invite(team, request.user):
        if request.method == "POST":
            form = TeamInvitationForm(request.POST, team=team)
            if form.is_valid():
                form.invite()
                messages.success(request, "Invitation created.")
                return redirect("team_detail", slug=slug)
        else:
            form = TeamInvitationForm(team=team)
    else:
        form = None
    
    return render(request, "teams/team_detail.html", {
        "team": team,
        "state": state,
        "invite_form": form,
        "can_join": can_join(team, request.user),
        "can_leave": can_leave(team, request.user),
        "can_apply": can_apply(team, request.user),
    })


@login_required
def team_join(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.get_state_for_user(request.user)
    if team.access == "invitation" and state is None and not request.user.is_staff:
        raise Http404()
    
    if can_join(team, request.user) and request.method == "POST":
        membership, created = Membership.objects.get_or_create(team=team, user=request.user)
        membership.state = "member"
        membership.save()
        messages.success(request, "Joined team.")
        return redirect("team_detail", slug=slug)
    else:
        return redirect("team_detail", slug=slug)


@login_required
def team_leave(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.get_state_for_user(request.user)
    if team.access == "invitation" and state is None and not request.user.is_staff:
        raise Http404()
    
    if can_leave(team, request.user) and request.method == "POST":
        membership = Membership.objects.get(team=team, user=request.user)
        membership.delete()
        messages.success(request, "Left team.")
        return redirect("dashboard")
    else:
        return redirect("team_detail", slug=slug)


@login_required
def team_apply(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.get_state_for_user(request.user)
    if team.access == "invitation" and state is None and not request.user.is_staff:
        raise Http404()
    
    if can_apply(team, request.user) and request.method == "POST":
        membership, created = Membership.objects.get_or_create(team=team, user=request.user)
        membership.state = "applied"
        membership.save()
        messages.success(request, "Applied to join team.")
        return redirect("team_detail", slug=slug)
    else:
        return redirect("team_detail", slug=slug)


@login_required
def team_promote(request, pk):
    if request.method == "POST":
        membership = get_object_or_404(Membership, pk=pk)
        state = membership.team.get_state_for_user(request.user)
        if request.user.is_staff or state == "manager":
            if membership.state == "member":
                membership.state = "manager"
                membership.save()
                messages.success(request, "Promoted to manager.")
    return redirect("team_detail", slug=membership.team.slug)


@login_required
def team_demote(request, pk):
    if request.method == "POST":
        membership = get_object_or_404(Membership, pk=pk)
        state = membership.team.get_state_for_user(request.user)
        if request.user.is_staff or state == "manager":
            if membership.state == "manager":
                membership.state = "member"
                membership.save()
                messages.success(request, "Demoted from manager.")
    return redirect("team_detail", slug=membership.team.slug)


@login_required
def team_accept(request, pk):
    if request.method == "POST":
        membership = get_object_or_404(Membership, pk=pk)
        state = membership.team.get_state_for_user(request.user)
        if request.user.is_staff or state == "manager":
            if membership.state == "applied":
                membership.state = "member"
                membership.save()
                messages.success(request, "Accepted application.")
    return redirect("team_detail", slug=membership.team.slug)


@login_required
def team_reject(request, pk):
    if request.method == "POST":
        membership = get_object_or_404(Membership, pk=pk)
        state = membership.team.get_state_for_user(request.user)
        if request.user.is_staff or state == "manager":
            if membership.state == "applied":
                membership.state = "rejected"
                membership.save()
                messages.success(request, "Rejected application.")
    return redirect("team_detail", slug=membership.team.slug)
