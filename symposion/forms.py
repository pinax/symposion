from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import account.forms


class SignupForm(account.forms.SignupForm):

    first_name = forms.CharField()
    last_name = forms.CharField()
    email_confirm = forms.EmailField(label="Confirm Email")

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        del self.fields["username"]
        self.fields.keyOrder = [
            "email",
            "email_confirm",
            "first_name",
            "last_name",
            "password",
            "password_confirm"
        ]

    def clean_email_confirm(self):
        email = self.cleaned_data.get("email")
        email_confirm = self.cleaned_data["email_confirm"]
        if email:
            if email != email_confirm:
                raise forms.ValidationError(
                    "Email address must match previously typed email address")
        return email_confirm


def get_language_choices():
    # In settings, we had to mark the language names for translation using
    # a dummy ugettext to avoid circular imports, so now we need to actually
    # retrieve their translations
    return [(value, _(name))
            for value, name
            in settings.LANGUAGES]


class LanguageForm(forms.Form):
    language = forms.ChoiceField(
        choices=get_language_choices(),
        help_text=_(u"Change language for this session")
    )
