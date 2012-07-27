from django import forms

from markitup.widgets import MarkItUpWidget

from symposion.reviews.models import Review, Comment, ProposalMessage, VOTES


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["vote", "comment"]
        widgets = { "comment": MarkItUpWidget() }
    
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields["vote"] = forms.ChoiceField(
            widget = forms.RadioSelect(),
            choices = VOTES.CHOICES
        )


class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = { "text": MarkItUpWidget() }


class SpeakerCommentForm(forms.ModelForm):
    class Meta:
        model = ProposalMessage
        fields = ["message"]
        widgets = { "message": MarkItUpWidget() }


class BulkPresentationForm(forms.Form):
    talk_ids = forms.CharField(
        max_length=500,
        help_text="Provide a comma seperated list of talk ids to accept."
    )
