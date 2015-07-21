import random

from django.core.exceptions import ValidationError
from django.conf import settings
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

import account.views

import symposion.forms

UNIQUE_EMAIL = getattr(settings, 'ACCOUNT_UNIQUE_EMAIL', True)


class SignupView(account.views.SignupView):

    form_class = symposion.forms.SignupForm
    form_kwargs = {
        "prefix": "signup",
    }

    def create_user(self, form, commit=True):
        user_kwargs = {
            "first_name": form.cleaned_data["first_name"],
            "last_name": form.cleaned_data["last_name"]
        }
        return super(SignupView, self).create_user(form, commit=commit,
                                                   **user_kwargs)

    def generate_username(self, form):
        def random_username():
            m = form.cleaned_data["email"]
            # don't ask
            n = random.randint(1, (10 ** (5 - 1)) - 1)
            return "%s%d" % (m, n)

        # username = email in most case.
        username = form.cleaned_data["email"]
        if not User.objects.filter(username=username):
            return username

        if UNIQUE_EMAIL:
            # wish not to happen but will happen
            # when user change its email and
            # re-use it when another singup
            # It is nothing to do special
            pass

        # fall back to add random number
        for i in range(1, 2 * (10 ** (5 - 1))):
            username = random_username()
            if not User.objects.filter(username=username):
                return username

        # no way
        raise ValidationError(_("Cannot process your signup request properly. "
                                "Please signup again with another email address."))


class LoginView(account.views.LoginView):

    form_class = account.forms.LoginEmailForm
    form_kwargs = {
        "prefix": "login",
    }


@login_required
def dashboard(request):
    if request.session.get("pending-token"):
        return redirect("speaker_create_token",
                        request.session["pending-token"])
    return render(request, "dashboard.html")
