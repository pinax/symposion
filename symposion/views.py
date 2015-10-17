from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from account.decorators import login_required


@login_required
def dashboard(request):
    if request.session.get("pending-token"):
        return redirect("speaker_create_token", request.session["pending-token"])
    return render(request, "dashboard.html")


@login_required
def user_list(request):
    if not request.user.is_staff:
        raise Http404()
    return render(request, "symposion/user_list.html", {
        "users": User.objects.all(),
    })
