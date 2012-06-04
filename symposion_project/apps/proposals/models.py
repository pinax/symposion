import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django import forms


class Proposal(models.Model):
    """
    A proposal represents a possible future session as it will be used before
    and during the review process. It has one mandatory speaker and possible
    additional speakers as well as a certain kind (tutorial, session, ...),
    audience level and proposed duration.

    TODO: Add tags to proposal which will then be copied over to the actual
          session.
    """
    conference = models.ForeignKey("conference.Conference",
        verbose_name="conference")
    title = models.CharField(_("title"), max_length=100)
    description = models.TextField(_("description"), max_length=400)
    abstract = models.TextField(_("abstract"))
    speaker = models.ForeignKey("speakers.Speaker", related_name="proposals",
        verbose_name=_("speaker"))
    additional_speakers = models.ManyToManyField("speakers.Speaker",
        blank=True, null=True, related_name="proposal_participations",
        verbose_name=_("additional speakers"))
    submission_date = models.DateTimeField(_("submission date"), editable=False,
        default=datetime.datetime.utcnow)
    modified_date = models.DateTimeField(_("modification date"), blank=True,
        null=True)
    kind = models.ForeignKey("conference.SessionKind",
        verbose_name=_("kind"))
    audience_level = models.ForeignKey("conference.AudienceLevel",
        verbose_name=_("audience level"))
    duration = models.ForeignKey("conference.SessionDuration",
        verbose_name=_("duration"))

    class Meta(object):
        verbose_name = _("proposal")
        verbose_name_plural = _("proposals")

    def clean(self):
        super(Proposal, self).clean()
        try:
            if self.conference is not None and self.duration.conference != self.conference:
                raise forms.ValidationError(_("The duration has to be associated with the same conference as the proposal"))
        except:
            pass

    def get_absolute_url(self):
        return reverse("view_proposal", kwargs=dict(pk=self.pk))
