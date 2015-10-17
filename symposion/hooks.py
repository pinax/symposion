from django.db import models
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.contrib.auth.models import User
from django.contrib.sites.models import Site


class DefaultHookSet(object):

    def __init__(self):
        from .conf import settings  # if put globally there is a race condition
        self.settings = settings

    def create_assignments(cls, proposal, origin):
        speakers = [proposal.speaker] + list(proposal.additional_speakers.all())
        reviewers = User.objects.exclude(
            pk__in=[
                speaker.user_id
                for speaker in speakers
                if speaker.user_id is not None
            ] + [
                assignment.user_id
                for assignment in cls.objects.filter(
                    submission=proposal
                )
            ]
        ).filter(
            groups__name="reviewers",
        ).filter(
            Q(reviewassignment__opted_out=False) | Q(reviewassignment=None)
        ).annotate(
            num_assignments=models.Count("reviewassignment")
        ).order_by(
            "num_assignments", "?",
        )
        num_assigned_reviewers = cls.objects.filter(
            submission=proposal,
            opted_out=False
        ).count()
        for reviewer in reviewers[:max(0, cls.NUM_REVIEWERS - num_assigned_reviewers)]:
            cls._default_manager.create(
                submission=proposal,
                user=reviewer,
                origin=origin,
            )

    def parse_content(self, content):
        return self.settings.SYMPOSION_MARKUP_RENDERER(content)

    def send_email(self, to, kind, **kwargs):
        current_site = Site.objects.get_current()
        ctx = {
            "current_site": current_site,
            "STATIC_URL": self.settings.STATIC_URL,
        }
        ctx.update(kwargs.get("context", {}))
        subject = "[%s] %s" % (
            current_site.name,
            render_to_string("symposion/emails/%s/subject.txt" % kind, ctx).strip()
        )

        message_html = render_to_string("symposion/emails/%s/message.html" % kind, ctx)
        message_plaintext = strip_tags(message_html)

        from_email = self.settings.DEFAULT_FROM_EMAIL

        email = EmailMultiAlternatives(subject, message_plaintext, from_email, to)
        email.attach_alternative(message_html, "text/html")
        email.send()


class HookProxy(object):

    def __getattr__(self, attr):
        from .conf import settings  # if put globally there is a race condition
        return getattr(settings.SYMPOSION_HOOKSET, attr)


hookset = HookProxy()
