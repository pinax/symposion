import os

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.contrib.sites.models import Site


class Sender(object):
    ''' Class for sending e-mails under a templete prefix. '''

    def __init__(self, template_prefix):
        self.template_prefix = template_prefix

    def send_email(self, to, kind, **kwargs):
        ''' Sends an e-mail to the given address.

        to: The address
        kind: the ID for an e-mail kind; it should point to a subdirectory of
            self.template_prefix containing subject.txt and message.html, which
            are django templates for the subject and HTML message respectively.

        context: a context for rendering the e-mail.

        '''

        return __send_email__(self.template_prefix, to, kind, **kwargs)


send_email = Sender("symposion/emails").send_email


def __send_email__(template_prefix, to, kind, **kwargs):

    current_site = Site.objects.get_current()

    ctx = {
        "current_site": current_site,
        "STATIC_URL": settings.STATIC_URL,
    }
    ctx.update(kwargs.get("context", {}))
    subject_template = os.path.join(template_prefix, "%s/subject.txt" % kind)
    message_template = os.path.join(template_prefix, "%s/message.html" % kind)
    subject = "[%s] %s" % (
        current_site.name,
        render_to_string(subject_template, ctx).strip()
    )

    message_html = render_to_string(message_template, ctx)
    message_plaintext = strip_tags(message_html)

    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        bcc_email = settings.ENVELOPE_BCC_LIST
    except AttributeError:
        bcc_email = None

    email = EmailMultiAlternatives(subject, message_plaintext, from_email, to, bcc=bcc_email)
    email.attach_alternative(message_html, "text/html")
    email.send()
