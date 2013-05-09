from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from django.contrib.admin.widgets import AdminFileWidget

from symposion.sponsorship.models import Sponsor, SponsorBenefit


class SponsorApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        kwargs.update({
            "initial": {
                "contact_name": self.user.get_full_name,
                "contact_email": self.user.email,
            }
        })
        super(SponsorApplicationForm, self).__init__(*args, **kwargs)
        if not self.user.is_staff:
            del self.fields["active"]
    
    class Meta:
        model = Sponsor
        fields = [
            "name",
            "external_url",
            "contact_name",
            "contact_email",
            "level",
            "active"
        ]
    
    def save(self, commit=True):
        obj = super(SponsorApplicationForm, self).save(commit=False)
        obj.applicant = self.user
        if commit:
            obj.save()
        return obj


class SponsorDetailsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(SponsorDetailsForm, self).__init__(*args, **kwargs)
        if not self.user.is_staff:
            del self.fields["active"]

    class Meta:
        model = Sponsor
        fields = [
            "name",
            "external_url",
            "contact_name",
            "contact_email",
            "active"
        ]


class SponsorBenefitsInlineFormSet(BaseInlineFormSet):
    
    def _construct_form(self, i, **kwargs):
        form = super(SponsorBenefitsInlineFormSet, self)._construct_form(i, **kwargs)
        
        # only include the relevant data fields for this benefit type
        fields = form.instance.data_fields()
        form.fields = dict((k, v) for (k, v) in form.fields.items() if k in fields + ["id"])
        
        for field in fields:
            # don't need a label, the form template will label it with the benefit name
            form.fields[field].label = ""
            
            # provide word limit as help_text
            if form.instance.benefit.type == "text" and form.instance.max_words:
                form.fields[field].help_text = u"maximum %s words" % form.instance.max_words
            
            # use admin file widget that shows currently uploaded file
            if field == "upload":
                form.fields[field].widget = AdminFileWidget()
        
        return form


SponsorBenefitsFormSet = inlineformset_factory(
    Sponsor, SponsorBenefit,
    formset=SponsorBenefitsInlineFormSet,
    can_delete=False, extra=0,
    fields=["text", "upload"]
)
