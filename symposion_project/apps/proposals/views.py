import urlparse

from django.views import generic as generic_views
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib import messages

from conference.models import current_conference

from . import forms
from . import models


class NextRedirectMixin(object):
    """
    A simple mixin for checking for a next parameter for redirects.
    """
    redirect_param = 'next'

    def get_next_redirect(self):
        next = self.request.GET.get(self.redirect_param)
        netloc = urlparse.urlparse(next)[1]
        if netloc is None or netloc == "" or netloc == self.request.get_host():
            return next
        return None


class SubmitProposalView(generic_views.CreateView, NextRedirectMixin):
    """
    Once registered a user can submit a proposal for the conference for a
    specific kind. This is only possible while the selected SessionKind
    accepts submissions.
    """
    form_class = forms.ProposalSubmissionForm
    model = models.Proposal

    def get_success_url(self):
        next = self.get_next_redirect()
        if next:
            return next
        return super(SubmitProposalView, self).get_success_url()

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

    def get_context_data(self, **kwargs):
        data = super(SingleProposalView, self).get_context_data(**kwargs)
        data['can_leave'] = self.request.user in [s.user for s in self.object.additional_speakers.all()]
        data['can_edit'] = self.request.user == self.object.speaker.user
        data['can_delete'] = self.request.user.is_staff or self.request.user == self.object.speaker.user
        return data


class PermissionCheckedUpdateView(generic_views.UpdateView, NextRedirectMixin):
    """
    Base update class that extends the UpdateView with an additional call
    of check_permissions.
    """
    def get_success_url(self):
        next = self.get_next_redirect()
        if next:
            return next
        return super(SubmitProposalView, self).get_success_url()

    def get_context_data(self, *args, **kwargs):
        ctx = super(PermissionCheckedUpdateView, self).get_context_data(*args, **kwargs)
        ctx.update({
            'next': self.get_success_url()
            })
        return ctx

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


class AbstractProposalAction(generic_views.DetailView, NextRedirectMixin):
    model = models.Proposal

    def check_permissions(self):
        pass

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        resp = self.check_permissions()
        if resp is not None:
            return resp
        return super(AbstractProposalAction, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        resp = self.check_permissions()
        if resp is not None:
            return resp
        resp = self.action()
        if resp is not None:
            return resp
        return HttpResponseRedirect(self.get_post_action_url())

    def get_context_data(self, *args, **kwargs):
        ctx = super(AbstractProposalAction, self).get_context_data(*args, **kwargs)
        ctx.update({
            'next': self.get_post_action_url()
            })
        return ctx

    def get_post_action_url(self):
        next = self.get_next_redirect()
        if next:
            return next
        return reverse('my_proposals')


class CancelProposalView(AbstractProposalAction):
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

    def action(self):
        self.object.delete()
        messages.success(self.request, _("Proposal has been removed"))
        return None


class LeaveProposalView(CancelProposalView):
    """
    A secondary speaker can decide not to actually take part in a session
    and therefor leave a proposal. This is an option that is exclusive
    to secondary speakers and is not available to the primary speaker.
    """
    template_name_suffix = "_leave_confirm"

    def check_permissions(self):
        user = self.request.user
        kind = self.object.kind
        if not kind.accepts_proposals():
            messages.error(self.request, _("You can no longer leave this proposal because the submission period has already ended."))
            return HttpResponseRedirect(self.object.get_absolute_url())
        if user not in [s.user for s in self.object.additional_speakers.all()]:
            messages.error(self.request, _("Only secondary speakers can leave a proposal"))
            return HttpResponseRedirect(self.object.get_absolute_url())
        return None

    def action(self):
        self.object.additional_speakers.remove(self.request.user.speaker_profile)
        messages.success(self.request, _("You were successfully removed as secondary speaker."))


class ListUserProposalsView(generic_views.TemplateView):
    """
    A speaker can see and manage a list of proposals submitted by her or that
    include her as a secondary speaker.
    """
    template_name = 'proposals/proposal_list_mine.html'

    def get_context_data(self, **kwargs):
        this_speaker = self.request.user.speaker_profile
        ctx = super(ListUserProposalsView, self).get_context_data(**kwargs)
        ctx.update({
            'proposals': this_speaker.proposals.all(),
            'proposal_participations': this_speaker.proposal_participations.all()
            })
        return ctx
