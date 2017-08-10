from __future__ import unicode_literals
from django import forms

from symposion.speakers.models import DefaultSpeaker


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
