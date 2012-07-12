from django import forms

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
                raise forms.ValidationError("Email address must match previously typed email address")
        return email_confirm
