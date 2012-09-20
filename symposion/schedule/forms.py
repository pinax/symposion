from django import forms
from django.db.models import Q

from symposion.schedule.models import Presentation


class SlotEditForm(forms.Form):
    
    presentation = forms.ModelChoiceField(queryset=Presentation.objects.none())
    
    def __init__(self, *args, **kwargs):
        content = kwargs.pop("content", None)
        if content:
            kwargs.setdefault("initial", {})["presentation"] = content
        super(SlotEditForm, self).__init__(*args, **kwargs)
        queryset = Presentation.objects.exclude(cancelled=True).order_by("proposal_base__pk")
        if content:
            queryset = queryset.filter(Q(slot=None) | Q(pk=content.pk))
            self.fields["presentation"].required = False
        else:
            queryset = queryset.filter(slot=None)
            self.fields["presentation"].required = True
        self.fields["presentation"].queryset = queryset
