from django import forms

from symposion.schedule.models import Slot, Presentation


class SlotEditForm(forms.Form):
    
    presentation = forms.ModelChoiceField(
        queryset=Presentation.objects.filter(slot__isnull=True),
        required=True,
    )
    slot_pk = forms.CharField(
        max_length=10,
        widget=forms.HiddenInput,
        required=True,
    )
    
    def clean_slot_pk(self):
        value = self.cleaned_data["slot_pk"]
        try:
            Slot.objects.get(pk=value)
        except Slot.DoesNotExist:
            raise forms.ValidationError("Invalid slot.")
        return value
