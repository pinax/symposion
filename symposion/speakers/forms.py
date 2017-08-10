from __future__ import unicode_literals
from django import forms

from symposion.speakers.models import DefaultSpeaker
from symposion.utils.loader import object_from_settings

def speaker_form():
    default = "symposion.speakers.forms.DefaultSpeakerForm"
    return object_from_settings("SYMPOSION_SPEAKER_FORM", default)


class DefaultSpeakerForm(forms.ModelForm):

    class Meta:
        model = DefaultSpeaker
        fields = [
            "name",
            "biography",
            "photo",
            "twitter_username",
        ]

    def clean_twitter_username(self):
        value = self.cleaned_data["twitter_username"]
        if value.startswith("@"):
            value = value[1:]
        return value
