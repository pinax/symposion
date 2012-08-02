from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from symposion.teams.models import Team, Membership


## perm checks
#
# @@@ these can be moved

def can_join(team, user):
    state = team.get_state_for_user(user)

    if team.access == "open" and state is None:
        return True
    elif team.access == "invitation" and state is "invited":
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
    elif user.is_staff and state is None:
        return True
    else:
        return False


## views


@login_required
def team_detail(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.get_state_for_user(request.user)
    if team.access == "invitation" and state is None and request.user.is_staff:
        raise Http404()
    
    return render(request, "teams/team_detail.html", {
        "team": team,
        "state": state,
        "can_join": can_join(team, request.user),
        "can_leave": can_leave(team, request.user),
        "can_apply": can_apply(team, request.user),
    })


@login_required
def team_join(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.get_state_for_user(request.user)
    if team.access == "invitation" and state is None and request.user.is_staff:
        raise Http404()
    
    if can_join(team, request.user) and request.method == "POST":
        membership, created = Membership.objects.get_or_create(team=team, user=request.user)
        membership.state = "member"
        membership.save()
        # contrib.message
        return redirect("team_detail", slug=slug)
    else:
        return redirect("team_detail", slug=slug)


@login_required
def team_leave(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.get_state_for_user(request.user)
    if team.access == "invitation" and state is None and request.user.is_staff:
        raise Http404()
    
    if can_leave(team, request.user) and request.method == "POST":
        membership = Membership.objects.get(team=team, user=request.user)
        membership.delete()
        # contrib.message
        return redirect("dashboard")
    else:
        return redirect("team_detail", slug=slug)


@login_required
def team_apply(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.get_state_for_user(request.user)
    if team.access == "invitation" and state is None and request.user.is_staff:
        raise Http404()
    
    if can_apply(team, request.user) and request.method == "POST":
        membership, created = Membership.objects.get_or_create(team=team, user=request.user)
        membership.state = "applied"
        membership.save()
        # contrib.message
        return redirect("team_detail", slug=slug)
    else:
        return redirect("team_detail", slug=slug)
