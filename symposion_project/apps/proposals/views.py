from django.views import generic as generic_views
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from conference.models import current_conference

from . import forms
from . import models


class SubmitProposalView(generic_views.CreateView):
    """
    Once registered a user can submit a proposal for the conference for a
    specific kind. This is only possible while the selected SessionKind
    accepts submissions.
    """
    form_class = forms.ProposalSubmissionForm
    model = models.Proposal

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.speaker = self.request.user.speaker_profile
        obj.conference = current_conference()
        obj.save()
        self.object = obj
        return HttpResponseRedirect(self.get_success_url())


class SingleProposalView(generic_views.DetailView):
    """
    Proposals can be viewed by everyone but provide some special links for
    administrators and people participating in this proposal.
    """
    model = models.Proposal

    def get_queryset(self):
        return self.model.objects.filter(conference=current_conference())


class PermissionCheckedUpdateView(generic_views.UpdateView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        resp = self.check_permissions()
        if resp is not None:
            return resp
        return super(PermissionCheckedUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        resp = self.check_permissions()
        if resp is not None:
            return resp
        return super(PermissionCheckedUpdateView, self).post(request, *args, **kwargs)


class EditProposalView(PermissionCheckedUpdateView):
    """
    The primary speaker can edit a proposal as long as the SessionKind
    still accepts proposals.
    """
    form_class = forms.ProposalSubmissionForm
    model = models.Proposal

    def check_permissions(self):
        """
        Only the primary speaker and staff members can edit a proposal.
        """
        user = self.request.user
        kind = self.object.kind
        if not kind.accepts_proposals():
            messages.error(self.request, _("You can no longer edit this proposal because the submission period has already ended."))
            return HttpResponseRedirect(self.object.get_absolute_url())
        if user != self.object.speaker.user and not user.is_staff:
            messages.error(self.request, _("You have to be the primary speaker mentioned in the proposal in order to edit it."))
            return HttpResponseRedirect(self.object.get_absolute_url())
        return None


class CancelProposalView(generic_views.DetailView):
    """
    During the submission and review period a proposal can be cancelled
    by the primary speaker. As soon as the review period is over
    and the proposal got accepted, an cancellation has to be communicated
    to the relevant staff member since this will involve rescheduling
    of other sessions.
    """
    template_name_suffix = '_cancel_confirm'
    model = models.Proposal

    def check_permissions(self):
        user = self.request.user
        kind = self.object.kind
        if not kind.accepts_proposals():
            messages.error(self.request, _("You can no longer cancel this proposal because the submission period has already ended."))
            return HttpResponseRedirect(self.object.get_absolute_url())
        if user != self.object.speaker.user:
            messages.error(self.request, _("You have to be the primary speaker mentioned in the proposal in order to cancel it."))
            return HttpResponseRedirect(self.object.get_absolute_url())
        return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        resp = self.check_permissions()
        if resp is not None:
            return resp
        return super(CancelProposalView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        resp = self.check_permissions()
        if resp is not None:
            return resp
        self.object.delete()
        messages.success(self.request, _("Proposal has been removed"))
        return HttpResponseRedirect('/')


class LeaveProposalView(generic_views.View):
    """
    A secondary speaker can decide not to actually take part in a session
    and therefor leave a proposal. This is an option that is exclusive
    to secondary speakers and is not available to the primary speaker.
    """
    pass


class ListProposalsView(generic_views.ListView):
    """
    A speaker can see and manage a list of proposal submitted by her or that
    includes her as secondary speaker.
    """
    pass
