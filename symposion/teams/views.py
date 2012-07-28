from django.http import Http404
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required

from symposion.teams.models import Team


@login_required
def team_detail(request, slug):
    team = get_object_or_404(Team, slug=slug)
    if team.get_state_for_user(request.user) != "manager":
        raise Http404()

    return render(request, "teams/team_detail.html", {
    })
