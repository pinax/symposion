from django import forms

from markitup.widgets import MarkItUpWidget

from pycon.models import PyConProposalCategory, PyConTalkProposal, PyConTutorialProposal, PyConPosterProposal


class PyConProposalForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(PyConProposalForm, self).__init__(*args, **kwargs)
        self.fields["category"] = forms.ModelChoiceField(
            queryset = PyConProposalCategory.objects.order_by("name")
        )
    
    def clean_description(self):
        value = self.cleaned_data["description"]
        if len(value) > 400:
            raise forms.ValidationError(
                u"The description must be less than 400 characters"
            )
        return value


class PyConTalkProposalForm(PyConProposalForm):

    class Meta:
        model = PyConTalkProposal
        fields = [
            "title",
            "category",
            "audience_level",
            "extreme",
            "duration",
            "description",
            "abstract",
            "additional_notes",
            "recording_release",
        ]
        widgets = {
            "abstract": MarkItUpWidget(),
            "additional_notes": MarkItUpWidget(),
        }


class PyConTutorialProposalForm(PyConProposalForm):

    class Meta:
        model = PyConTutorialProposal
        fields = [
            "title",
            "category",
            "audience_level",
            "description",
            "abstract",
            "additional_notes",
            "recording_release",

        ]
        widgets = {
            "abstract": MarkItUpWidget(),
            "additional_notes": MarkItUpWidget(),
        }


class PyConPosterProposalForm(PyConProposalForm):

    class Meta:
        model = PyConPosterProposal
        fields = [
            "title",
            "category",
            "audience_level",
            "description",
            "abstract",
            "additional_notes",
            "recording_release",

        ]
        widgets = {
            "abstract": MarkItUpWidget(),
            "additional_notes": MarkItUpWidget(),
        }

