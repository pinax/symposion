from django import forms
from django.utils.translation import ugettext_lazy as _

from conference.models import current_conference
from conference import models as conference_models

from . import models


class ProposalSubmissionForm(forms.ModelForm):
    class Meta(object):
        model = models.Proposal
        fields = [
            "kind",
            "title",
            "description",
            "abstract",
            "additional_speakers",
            "audience_level",
            "duration",
        ]

    def __init__(self, *args, **kwargs):
        super(ProposalSubmissionForm, self).__init__(*args, **kwargs)
        self.fields['kind'] = forms.ModelChoiceField(queryset=conference_models.SessionKind.objects.filter(conference=current_conference()))
        self.fields['audience_level'] = forms.ModelChoiceField(queryset=conference_models.AudienceLevel.objects.filter(conference=current_conference()))
        self.fields['duration'] = forms.ModelChoiceField(queryset=conference_models.SessionDuration.objects.filter(conference=current_conference()))

    def clean(self):
        cleaned_data = super(ProposalSubmissionForm, self).clean()
        kind = cleaned_data.get('kind')
        if kind is not None and not kind.accepts_proposals():
            raise forms.ValidationError(_("The selected session kind doesn't accept any proposals anymore."))
        return cleaned_data

    def clean_audience_level(self):
        value = self.cleaned_data["audience_level"]
        if value.conference != current_conference():
            raise forms.ValidationError(_("Please select a valid audience level."))
        return value

    def clean_duration(self):
        value = self.cleaned_data["duration"]
        if value.conference != current_conference():
            raise forms.ValidationError(_("Please select a valid duration."))
        return value

    def clean_kind(self):
        value = self.cleaned_data["kind"]
        if value.conference != current_conference():
            raise forms.ValidationError(_("Please select a valid session kind."))
        return value


class ProposalUpdateForm(object):
    pass
