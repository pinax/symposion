from django import forms

from django.contrib import messages

from markitup.widgets import MarkItUpWidget

from symposion.speakers.models import Speaker


class SpeakerForm(forms.ModelForm):
    
    sessions_preference = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=Speaker.SESSION_COUNT_CHOICES,
        required=False,
        help_text="If you've submitted multiple proposals, please let us know if you only want to give one or if you'd like to give two talks."
    )
    
    class Meta:
        model = Speaker
        fields = [
            "name",
            "biography",
            "photo",
            "twitter_username",
            "sessions_preference"
        ]
        widgets = {
            "biography": MarkItUpWidget(),
        }
    
    def clean_twitter_username(self):
        value = self.cleaned_data["twitter_username"]
        if value.startswith("@"):
            value = value[1:]
        return value
    
    def clean_sessions_preference(self):
        value = self.cleaned_data["sessions_preference"]
        if not value:
            return None
        return int(value)


# class SignupForm(PinaxSignupForm):
    
#     def save(self, speaker, request=None):
#         # don't assume a username is available. it is a common removal if
#         # site developer wants to use email authentication.
#         username = self.cleaned_data.get("username")
#         email = self.cleaned_data["email"]
#         new_user = self.create_user(username)
#         if speaker.invite_email == new_user.email:
#             # already verified so can just create
#             EmailAddress(user=new_user, email=email, verified=True, primary=True).save()
#         else:
#             if request:
#                 messages.info(request, u"Confirmation email sent to %(email)s" % {"email": email})
#             EmailAddress.objects.add_email(new_user, email)
#             new_user.is_active = False
#             new_user.save()
#         self.after_signup(new_user)
#         return new_user
