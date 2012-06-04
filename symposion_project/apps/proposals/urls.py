from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = patterns('',
    url(r'^submit/$',
        login_required(views.SubmitProposalView.as_view()),
        name='submit_proposal'),
    url(r"^view/(?P<pk>\d+)/",
        views.SingleProposalView.as_view(),
        name="view_proposal"),
    url(r"^edit/(?P<pk>\d+)/",
        login_required(views.EditProposalView.as_view()),
        name="edit_proposal"),
    url(r"^cancel/(?P<pk>\d+)/",
        login_required(views.CancelProposalView.as_view()),
        name="cancel_proposal"),
    url(r"^leave/(?P<pk>\d+)/",
        login_required(views.LeaveProposalView.as_view()),
        name="leave_proposal"),
    url(r"^mine/$",
        login_required(views.ListUserProposalsView.as_view()),
        name="my_proposals"),
    )
