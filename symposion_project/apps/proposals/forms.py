from django import forms
from django.utils.translation import ugettext_lazy as _

from . import models


class ProposalSubmissionForm(forms.ModelForm):
    class Meta(object):
        model = models.Proposal

    def clean(self):
        cleaned_data = super(ProposalSubmissionForm, self).clean()
        kind = cleaned_data.get('kind')
        if kind is not None and not kind.accepts_proposals():
            raise forms.ValidationError(_("The selected session kind doesn't accept any proposals anymore."))
        return cleaned_data


class ProposalUpdateForm(object):
    pass