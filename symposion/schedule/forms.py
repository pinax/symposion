from django import forms
from django.db.models import Q

from symposion.schedule.models import Presentation


class SlotEditForm(forms.Form):
    
    presentation = forms.ModelChoiceField(
        queryset=Presentation.objects.all(),
        required=True,
    )
    
    def __init__(self, *args, **kwargs):
        presentation = kwargs.get("initial", {}).get("presentation")
        super(SlotEditForm, self).__init__(*args, **kwargs)
        queryset = self.fields["presentation"].queryset
        if presentation:
            queryset = queryset.filter(Q(slot=None) | Q(pk=presentation.pk))
        else:
            queryset = queryset.filter(slot=None)
        self.fields["presentation"].queryset = queryset
