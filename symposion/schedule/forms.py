from django import forms
from django.db.models import Q

from markitup.widgets import MarkItUpWidget

from symposion.schedule.models import Presentation


class SlotEditForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.slot = kwargs.pop("slot")
        super(SlotEditForm, self).__init__(*args, **kwargs)
        if self.slot.kind.label in ["talk", "tutorial"]:
            self.fields["presentation"] = self.build_presentation_field()
        else:
            self.fields["content_override"] = self.build_content_override_field()
    
    def build_presentation_field(self):
        kwargs = {}
        queryset = Presentation.objects.all()
        queryset = queryset.exclude(cancelled=True)
        queryset = queryset.order_by("proposal_base__pk")
        if self.slot.content:
            queryset = queryset.filter(Q(slot=None) | Q(pk=self.slot.content.pk))
            kwargs["required"] = False
            kwargs["initial"] = self.slot.content
        else:
            queryset = queryset.filter(slot=None)
            kwargs["required"] = True
        kwargs["queryset"] = queryset
        return forms.ModelChoiceField(**kwargs)
    
    def build_content_override_field(self):
        kwargs = {
            "label": "Content",
            "widget": MarkItUpWidget(),
            "required": False,
            "initial": self.slot.content_override,
        }
        return forms.CharField(**kwargs)
