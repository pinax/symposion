from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now

from django.contrib.auth.models import User

from pinax.submissions.models import SubmissionBase, SubmissionKind
from timezone_field import TimeZoneField

from .hooks import hookset

CONFERENCE_CACHE = {}


@python_2_unicode_compatible
class Conference(models.Model):
    """
    the full conference for a specific year, e.g. US PyCon 2012.
    """

    title = models.CharField(_("Title"), max_length=100)

    # when the conference runs
    start_date = models.DateField(_("Start date"), null=True, blank=True)
    end_date = models.DateField(_("End date"), null=True, blank=True)

    # timezone the conference is in
    timezone = TimeZoneField(blank=True, verbose_name=_("timezone"))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Conference, self).save(*args, **kwargs)
        if self.id in CONFERENCE_CACHE:
            del CONFERENCE_CACHE[self.id]

    def delete(self):
        pk = self.pk
        super(Conference, self).delete()
        try:
            del CONFERENCE_CACHE[pk]
        except KeyError:
            pass

    class Meta(object):
        verbose_name = _("conference")
        verbose_name_plural = _("conferences")


@python_2_unicode_compatible
class Section(models.Model):
    """
    a section of the conference such as "Tutorials", "Workshops",
    "Talks", "Expo", "Sprints", that may have its own review and
    scheduling process.
    """

    conference = models.ForeignKey(Conference, verbose_name=_("Conference"))

    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(verbose_name=_("Slug"))

    # when the section runs
    start_date = models.DateField(_("Start date"), null=True, blank=True)
    end_date = models.DateField(_("End date"), null=True, blank=True)

    def __str__(self):
        return "%s %s" % (self.conference, self.name)

    class Meta(object):
        verbose_name = _("section")
        verbose_name_plural = _("sections")
        ordering = ["start_date"]


@python_2_unicode_compatible
class ProposalSection(models.Model):
    """
    configuration of proposal submissions for a specific Section.

    a section is available for proposals iff:
      * it is after start (if there is one) and
      * it is before end (if there is one) and
      * closed is NULL or False
    """

    section = models.OneToOneField(Section, verbose_name=_("Section"))

    start = models.DateTimeField(null=True, blank=True, verbose_name=_("Start"))
    end = models.DateTimeField(null=True, blank=True, verbose_name=_("End"))
    closed = models.NullBooleanField(verbose_name=_("Closed"))
    published = models.NullBooleanField(verbose_name=_("Published"))

    @classmethod
    def available(cls):
        return cls._default_manager.filter(
            Q(start__lt=now()) | Q(start=None),
            Q(end__gt=now()) | Q(end=None),
            Q(closed=False) | Q(closed=None),
        )

    def is_available(self):
        if self.closed:
            return False
        if self.start and self.start > now():
            return False
        if self.end and self.end < now():
            return False
        return True

    def __str__(self):
        return self.section.name


@python_2_unicode_compatible
class ProposalKind(SubmissionKind):
    """
    e.g. talk vs panel vs tutorial vs poster

    Note that if you have different deadlines, reviewers, etc. you'll want
    to distinguish the section as well as the kind.
    """

    section = models.ForeignKey(Section, related_name="proposal_kinds", verbose_name=_("Section"))


@python_2_unicode_compatible
class ProposalBase(SubmissionBase):

    kind = models.ForeignKey(ProposalKind, verbose_name=_("Kind"))

    title = models.CharField(max_length=100, verbose_name=_("Title"))
    description = models.TextField(
        _("Brief Description"),
        max_length=400,  # @@@ need to enforce 400 in UI
        help_text=_("If your proposal is accepted this will be made public and printed in the "
                    "program. Should be one paragraph, maximum 400 characters.")
    )
    abstract = models.TextField(
        _("Detailed Abstract"),
        help_text=_("Detailed outline. Will be made public if your proposal is accepted. Edit "
                    "using <a href='http://daringfireball.net/projects/markdown/basics' "
                    "target='_blank'>Markdown</a>.")
    )
    abstract_html = models.TextField(blank=True)
    additional_notes = models.TextField(
        _("Addtional Notes"),
        blank=True,
        help_text=_("Anything else you'd like the program committee to know when making their "
                    "selection: your past experience, etc. This is not made public. Edit using "
                    "<a href='http://daringfireball.net/projects/markdown/basics' "
                    "target='_blank'>Markdown</a>.")
    )
    additional_notes_html = models.TextField(blank=True)

    speaker = models.ForeignKey("Speaker", related_name="proposals", verbose_name=_("Speaker"))

    # @@@ this validation used to exist as a validators keyword on additional_speakers
    #     M2M field but that is no longer supported by Django. Should be moved to
    #     the form level
    #def additional_speaker_validator(self, a_speaker):
    #    if a_speaker.speaker.email == self.speaker.email:
    #        raise ValidationError(_("%s is same as primary speaker.") % a_speaker.speaker.email)
    #    if a_speaker in [self.additional_speakers]:
    #        raise ValidationError(_("%s has already been in speakers.") % a_speaker.speaker.email)

    additional_speakers = models.ManyToManyField("Speaker", through="AdditionalSpeaker", blank=True, verbose_name=_("Addtional speakers"))

    def save(self, *args, **kwargs):
        self.abstract_html = hookset.parse_content(self.abstract)
        self.additional_notes_html = hookset.parse_content(self.additional_notes)
        return super(ProposalBase, self).save(*args, **kwargs)

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

    @property
    def status(self):
        try:
            return self.result.status
        except ObjectDoesNotExist:
            return _('Undecided')

    def speakers(self):
        yield self.speaker
        speakers = self.additional_speakers.exclude(
            additionalspeaker__status=AdditionalSpeaker.SPEAKING_STATUS_DECLINED)
        for speaker in speakers:
            yield speaker

    def notification_email_context(self):
        return {
            "title": self.title,
            "speaker": self.speaker.name,
            "speakers": ', '.join([x.name for x in self.speakers()]),
            "kind": self.kind.name,
        }

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Speaker(models.Model):

    SESSION_COUNT_CHOICES = [
        (1, "One"),
        (2, "Two")
    ]

    user = models.OneToOneField(User, null=True, related_name="speaker_profile", verbose_name=_("User"))
    name = models.CharField(verbose_name=_("Name"), max_length=100,
                            help_text=_("As you would like it to appear in the"
                                        " conference program."))
    biography = models.TextField(blank=True, help_text=_("A little bit about you.  Edit using Markdown"), verbose_name=_("Biography"))
    biography_html = models.TextField(blank=True)
    photo = models.ImageField(upload_to="speaker_photos", blank=True, verbose_name=_("Photo"))
    annotation = models.TextField(verbose_name=_("Annotation"))  # staff only
    invite_email = models.CharField(max_length=200, unique=True, null=True, db_index=True, verbose_name=_("Invite_email"))
    invite_token = models.CharField(max_length=40, db_index=True, verbose_name=_("Invite token"))
    created = models.DateTimeField(default=now, editable=False, verbose_name=_("Created"))

    class Meta:
        ordering = ['name']
        verbose_name = _("Speaker")
        verbose_name_plural = _("Speakers")

    def save(self, *args, **kwargs):
        self.biography_html = hookset.parse_content(self.biography)
        return super(Speaker, self).save(*args, **kwargs)

    def __str__(self):
        if self.user:
            return self.name
        else:
            return "?"

    def get_absolute_url(self):
        return reverse("speaker_edit")

    @property
    def email(self):
        if self.user is not None:
            return self.user.email
        else:
            return self.invite_email

    @property
    def all_presentations(self):
        presentations = []
        if self.presentations:
            for p in self.presentations.all():
                presentations.append(p)
            for p in self.copresentations.all():
                presentations.append(p)
        return presentations


@python_2_unicode_compatible
class AdditionalSpeaker(models.Model):

    SPEAKING_STATUS_PENDING = 1
    SPEAKING_STATUS_ACCEPTED = 2
    SPEAKING_STATUS_DECLINED = 3

    SPEAKING_STATUS = [
        (SPEAKING_STATUS_PENDING, _("Pending")),
        (SPEAKING_STATUS_ACCEPTED, _("Accepted")),
        (SPEAKING_STATUS_DECLINED, _("Declined")),
    ]

    speaker = models.ForeignKey(Speaker, verbose_name=_("Speaker"))
    proposalbase = models.ForeignKey(ProposalBase, verbose_name=_("Proposalbase"))
    status = models.IntegerField(choices=SPEAKING_STATUS, default=SPEAKING_STATUS_PENDING, verbose_name=_("Status"))

    class Meta:
        unique_together = ("speaker", "proposalbase")
        verbose_name = _("Addtional speaker")
        verbose_name_plural = _("Additional speakers")

    def __str__(self):
        if self.status is self.SPEAKING_STATUS_PENDING:
            return _(u"pending speaker (%s)") % self.speaker.email
        elif self.status is self.SPEAKING_STATUS_DECLINED:
            return _(u"declined speaker (%s)") % self.speaker.email
        else:
            return self.speaker.name


def current_conference():
    from django.conf import settings
    try:
        conf_id = settings.CONFERENCE_ID
    except AttributeError:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured("You must set the CONFERENCE_ID setting.")
    try:
        current_conf = CONFERENCE_CACHE[conf_id]
    except KeyError:
        current_conf = Conference.objects.get(pk=conf_id)
        CONFERENCE_CACHE[conf_id] = current_conf
    return current_conf
