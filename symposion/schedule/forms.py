from django import forms
from django.db.models import Q

from schedule.models import Plenary, Recess, Presentation


class PlenaryForm(forms.ModelForm):
    class Meta:
        model = Plenary
        exclude = ["slot", "additional_speakers"]


class RecessForm(forms.ModelForm):
    class Meta:
        model = Recess
        exclude = ["slot"]


def presentation_queryset(include=None):
    qs = Presentation.objects.all()
    qs = qs.filter(
        Q(presentation_type=Presentation.PRESENTATION_TYPE_TALK) |
        Q(presentation_type=Presentation.PRESENTATION_TYPE_PANEL)
    )
    if include:
        qs = qs.filter(Q(slot=None) | Q(pk=include.pk))
    else:
        qs = qs.filter(slot=None)
    qs = qs.order_by("pk")
    return qs


class PresentationModelChoiceField(forms.ModelChoiceField):
    
    def __init__(self, *args, **kwargs):
        kwargs["queryset"] = Presentation.objects.none()
        super(PresentationModelChoiceField, self).__init__(*args, **kwargs)
    
    def label_from_instance(self, obj):
        return u"%d: %s" % (obj.pk, obj.title)


class PresentationForm(forms.Form):
    
    presentation = PresentationModelChoiceField()
    
    def __init__(self, *args, **kwargs):
        presentation = kwargs.get("initial", {}).get("presentation", None)
        super(PresentationForm, self).__init__(*args, **kwargs)
        if presentation:
            self.fields["presentation"].queryset = presentation_queryset(include=presentation)
        else:
            self.fields["presentation"].queryset = presentation_queryset()
    
    def save(self, commit=True):
        return self.cleaned_data["presentation"]
