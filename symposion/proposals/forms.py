from django import forms
from django.db.models import Q

from proposals.models import Proposal, ProposalSessionType


class ProposalForm(forms.ModelForm):
    
    class Meta:
        model = Proposal
        exclude = [
            "speaker",
            "additional_speakers",
            "cancelled",
            "opt_out_ads",
            "invited",
        ]
    
    def __init__(self, *args, **kwargs):
        super(ProposalForm, self).__init__(*args, **kwargs)
        self.fields["session_type"] = forms.ModelChoiceField(
            queryset=ProposalSessionType.available()
        )
    
    def clean_description(self):
        value = self.cleaned_data["description"]
        if len(value) > 400:
            raise forms.ValidationError(
                u"The description must be less than 400 characters"
            )
        return value
    
    def clean_session_type(self):
        return self.cleaned_data["session_type"].pk


class ProposalSubmitForm(ProposalForm):
    pass


class ProposalEditForm(ProposalForm):
    pass


class AddSpeakerForm(forms.Form):
    
    email = forms.EmailField(
        label = "E-mail address of new speaker (use their e-mail address, not yours)"
    )
    
    def __init__(self, *args, **kwargs):
        self.proposal = kwargs.pop("proposal")
        super(AddSpeakerForm, self).__init__(*args, **kwargs)
    
    def clean_email(self):
        value = self.cleaned_data["email"]
        exists = self.proposal.additional_speakers.filter(
            Q(user=None, invite_email=value) |
            Q(user__email=value)
        ).exists()
        if exists:
            raise forms.ValidationError(
                "This e-mail address has already been added to your talk proposal"
            )
        return value
