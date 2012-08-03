from django import forms

from django.contrib.auth.models import User

from symposion.teams.models import Membership


class TeamInvitationForm(forms.Form):
    
    email = forms.EmailField(help_text="email address must be that of a user on the site")
    
    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop("team")
        super(TeamInvitationForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super(TeamInvitationForm, self).clean()
        email = cleaned_data.get("email")
        
        if email is None:
            raise forms.ValidationError("valid email address required")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # eventually we can invite them but for now assume they are
            # already on the site
            raise forms.ValidationError("no known user with email address %s" % email)
        
        state = self.team.get_state_for_user(user)
        
        if state in ["member", "manager"]:
            raise forms.ValidationError("user already in team")
        
        if state in ["invited"]:
            raise forms.ValidationError("user already invited to team")
        
        self.user = user
        self.state = state
        
        return cleaned_data
    
    def invite(self):
        if self.state is None:
            Membership.objects.create(team=self.team, user=self.user, state="invited")
        elif self.state == "applied":
            # if they applied we shortcut invitation process
            membership = Membership.objects.get(team=self.team, user=self.user)
            membership.state = "member"
            membership.save()
