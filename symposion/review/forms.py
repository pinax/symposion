from django import forms

from symposion.review.models import Review, Comment, ProposalMessage


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["vote", "comment"]


class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class SpeakerCommentForm(forms.ModelForm):
    class Meta:
        model = ProposalMessage
        fields = ["message"]
