from django import forms

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
