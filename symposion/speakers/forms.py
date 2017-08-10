from __future__ import unicode_literals
from django import forms

from symposion.speakers.models import speaker_model
from symposion.utils.loader import object_from_settings

def speaker_form():
    default = "symposion.speakers.forms.DefaultSpeakerForm"
    return object_from_settings("SYMPOSION_SPEAKER_FORM", default)

SpeakerModel = speaker_model()


class DefaultSpeakerForm(forms.ModelForm):

    class Meta:
        model = SpeakerModel
        exclude = [
            "user",
            "biography_html",
            "annotation",
            "invite_email",
            "invite_token",
            "created",
        ]
