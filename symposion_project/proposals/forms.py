from django import forms

from markitup.widgets import MarkItUpWidget

from symposion_project.proposals.models import TalkProposal, TutorialProposal, PosterProposal, LightningProposal


class ProposalForm(forms.ModelForm):
    
    def clean_description(self):
        value = self.cleaned_data["description"]
        if len(value) > 300:
            raise forms.ValidationError(
                u"The description must be no more than 300 characters"
            )
        return value


class TalkProposalForm(ProposalForm):

    class Meta:
        model = TalkProposal
        fields = [
            "title",
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


class TutorialProposalForm(ProposalForm):

    class Meta:
        model = TutorialProposal
        fields = [
            "title",
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


class LightningProposalForm(ProposalForm):

    class Meta:
        model = LightningProposal
        fields = [
            "title",
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


class PosterProposalForm(ProposalForm):

    class Meta:
        model = PosterProposal
        fields = [
            "title",
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
