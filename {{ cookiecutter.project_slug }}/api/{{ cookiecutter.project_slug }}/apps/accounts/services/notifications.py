import logging

from dataclasses import dataclass

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils.html import strip_tags


logger = logging.getLogger(__name__)


@dataclass
class NotificationHandlerConfig:
    # Unique identifier of the notification.
    # if no templates are specified, the templates will be named after this
    kind: str
    subject: str
    # Name of the template to use for the html version of the email.
    # It should be relative to the account/notifications directory.
    template_html_filename: str | None = None
    # Name of the template to use for the plain text version of the email.
    # It should be relative to the account/notifications directory.
    template_plain_filename: str | None = None
    # Email address to use as the sender of the email.
    from_email: str = settings.DEFAULT_FROM_EMAIL

    @property
    def template_html_name(self):
        filename = self.template_html_filename or f"{self.kind}.html"
        return f"accounts/notifications/{filename}"

    @property
    def template_plain_name(self):
        filename = self.template_plain_filename or f"{self.kind}.html"
        return f"accounts/notifications/{filename}"

    @property
    def html_only(self) -> bool:
        return self.template_plain_name == self.template_html_name


_HANDLERS = [
    NotificationHandlerConfig(
        kind="user-reset-password",
        subject="Reset your password",
    ),
]

HANDLERS = {handler.kind: handler for handler in _HANDLERS}


def notification(user_email: str, kind: str, context: dict) -> None:
    try:
        config = HANDLERS[kind]
    except KeyError:
        logger.warning("Attempted to send notification of unknown kind %s", kind)
        return

    template_html = get_template(config.template_html_name)
    template_plain = get_template(config.template_plain_name)

    message_html = template_html.render(context)

    if config.html_only:
        message_plain = strip_tags(message_html)
    else:
        message_plain = template_plain.render(context)

    res = send_mail(
        subject=config.subject,
        message=message_plain,
        from_email=config.from_email,
        recipient_list=[user_email],
        html_message=message_html,
    )

    if res != 1:
        logger.warning(f"Failed to send {kind} notification to user {user_email}")

    return
