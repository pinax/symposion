import datetime
import os
import uuid

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

import reversion

from markitup.fields import MarkupField

from model_utils.managers import InheritanceManager

from symposion.conference.models import Section


class ProposalSection(models.Model):
    """
    configuration of proposal submissions for a specific Section.
    
    a section is available for proposals iff:
      * it is after start (if there is one) and
      * it is before end (if there is one) and
      * closed is NULL or False
    """
    
    section = models.OneToOneField(Section)
    
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    closed = models.NullBooleanField()
    published = models.NullBooleanField()
    
    @classmethod
    def available(cls):
        now = datetime.datetime.now()
        return cls._default_manager.filter(
            Q(start__lt=now) | Q(start=None),
            Q(end__gt=now) | Q(end=None),
            Q(closed=False) | Q(closed=None),
        )
    
    def is_available(self):
        if self.closed:
            return False
        now = datetime.datetime.now()
        if self.start and self.start > now:
            return False
        if self.end and self.end < now:
            return False
        return True
    
    def __unicode__(self):
        return self.section.name


class ProposalKind(models.Model):
    """
    e.g. talk vs panel vs tutorial vs poster
    
    Note that if you have different deadlines, reviewers, etc. you'll want
    to distinguish the section as well as the kind.
    """
    
    section = models.ForeignKey(Section, related_name="proposal_kinds")
    
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField()
    
    def __unicode__(self):
        return self.name


class ProposalBase(models.Model):
    
    objects = InheritanceManager()
    
    kind = models.ForeignKey(ProposalKind)
    
    title = models.CharField(max_length=100)
    description = models.TextField(
        _("Brief Outline"),
        max_length=400,  # @@@ need to enforce 400 in UI
        help_text="If your talk is accepted this will be made public and printed in the program. Should be one paragraph, maximum 400 characters."
    )
    abstract = MarkupField(
        _("Detailed Abstract"),
        help_text=_("Detailed description and outline. Will be made public if your talk is accepted. Edit using <a href='http://daringfireball.net/projects/markdown/basics' target='_blank'>Markdown</a>.")
    )
    additional_notes = MarkupField(
        blank=True,
        help_text=_("Anything else you'd like the program committee to know when making their selection: your past speaking experience, open source community experience, etc. Edit using <a href='http://daringfireball.net/projects/markdown/basics' target='_blank'>Markdown</a>.")
    )
    submitted = models.DateTimeField(
        default=datetime.datetime.now,
        editable=False,
    )
    speaker = models.ForeignKey("speakers.Speaker", related_name="proposals")
    additional_speakers = models.ManyToManyField("speakers.Speaker", through="AdditionalSpeaker", blank=True)
    cancelled = models.BooleanField(default=False)
    
    def can_edit(self):
        return True
    
    @property
    def section(self):
        return self.kind.section
    
    @property
    def speaker_email(self):
        return self.speaker.email
    
    @property
    def number(self):
        return str(self.pk).zfill(3)
    
    def speakers(self):
        yield self.speaker
        for speaker in self.additional_speakers.exclude(additionalspeaker__status=AdditionalSpeaker.SPEAKING_STATUS_DECLINED):
            yield speaker
    
    def notification_email_context(self):
        return {
            "title": self.title,
            "speaker": self.speaker.name,
            "kind": self.kind.name,
        }


reversion.register(ProposalBase)


class AdditionalSpeaker(models.Model):
    
    SPEAKING_STATUS_PENDING = 1
    SPEAKING_STATUS_ACCEPTED = 2
    SPEAKING_STATUS_DECLINED = 3
    
    SPEAKING_STATUS = [
        (SPEAKING_STATUS_PENDING, _("Pending")),
        (SPEAKING_STATUS_ACCEPTED, _("Accepted")),
        (SPEAKING_STATUS_DECLINED, _("Declined")),
    ]
    
    speaker = models.ForeignKey("speakers.Speaker")
    proposalbase = models.ForeignKey(ProposalBase)
    status = models.IntegerField(choices=SPEAKING_STATUS, default=SPEAKING_STATUS_PENDING)
    
    class Meta:
        db_table = "proposals_proposalbase_additional_speakers"
        unique_together = ("speaker", "proposalbase")


def uuid_filename(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("document", filename)


class SupportingDocument(models.Model):
    
    proposal = models.ForeignKey(ProposalBase, related_name="supporting_documents")
    
    uploaded_by = models.ForeignKey(User)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    
    file = models.FileField(upload_to=uuid_filename)
    description = models.CharField(max_length=140)

    def download_url(self):
        return reverse("proposal_document_download", args=[self.pk, os.path.basename(self.file.name).lower()])
