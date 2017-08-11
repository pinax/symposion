from __future__ import unicode_literals
from django import forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from symposion.proposals.models import SupportingDocument


# @@@ generic proposal form

class ProposalMixIn(forms.Form):
    ''' A MixIn form that allows apps that subclass ProposalBase to set
    the abstract, description, or additional notes fields to be required.

    See proposals.rst for information.
    '''

    def _set_field_required(self, key, required):
        self.fields[key].required = required

    def abstract_required(self, required=True):
        self._set_field_required("abstract", required)

    def description_required(self, required=True):
        self._set_field_required("description", required)

    def additional_notes_required(self, required=True):
        self._set_field_required("additional_notes", required)


class AddSpeakerForm(forms.Form):

    email = forms.EmailField(
        label=_("Email address of new speaker (use their email address, not yours)")
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
                _("This email address has already been invited to your talk proposal")
            )
        return value


class SupportingDocumentCreateForm(forms.ModelForm):

    class Meta:
        model = SupportingDocument
        fields = [
            "file",
            "description",
        ]
