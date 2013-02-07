from django import forms

from markitup.widgets import MarkItUpWidget

from .models import Page


class PageForm(forms.ModelForm):
    
    class Meta:
        model = Page
        fields = ["title", "body", "path"]
        widgets = {
            "body": MarkItUpWidget(),
            "path": forms.HiddenInput(),
        }


class FileUploadForm(forms.Form):
    
    file = forms.FileField()
