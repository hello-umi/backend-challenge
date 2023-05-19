import logging
import os

from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail

from proxy.strategies.message_strategy import MessagingStrategy

logger = logging.getLogger(__name__)


class EmailMessagingStrategy(MessagingStrategy):
    """Email channel implementation. The following Environment Variables should be set:
    EMAIL_SUBJECT
    EMAIL_FROM_EMAIL or DEFAULT_FROM_EMAIL
    EMAIL_RECIPIENT_LIST

    otherwise the emails will fail.
    """

    def __init__(self):
        self.subject = os.getenv("EMAIL_SUBJECT", None)
        from_email = os.getenv("EMAIL_FROM_EMAIL", None)
        if not from_email:
            from_email = os.getenv(
                "DEFAULT_FROM_EMAIL",
            )
        self.from_email = from_email
        self.recipient_list = os.getenv("EMAIL_RECIPIENT_LIST", "").split(",")

        if not (self.subject and self.from_email and self.recipient_list):
            raise ImproperlyConfigured(
                "EMAIL Channel is missing one or more of their config. Make sure to set in the "
                "ENVIRONMENT EMAIL_SUBJECT, EMAIL_FROM_EMAIL, EMAIL_RECIPIENT_LIST"
            )

    def send_message(self, message):
        logger.info(f"Sending email: {message}")
        send_mail(self.subject, message, self.from_email, self.recipient_list)
        logger.info("Email sent!")
