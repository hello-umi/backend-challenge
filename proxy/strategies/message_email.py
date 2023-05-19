import logging
import os

from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail

from proxy.strategies.message_strategy import MessagingStrategy

logger = logging.getLogger(__name__)


class EmailMessagingStrategy(MessagingStrategy):
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

        from_email = "notifications@landbot.io"
        recipient_list = ["recipient1@example.com", "recipient2@example.com"]

        send_mail(self.subject, message, from_email, recipient_list)
        logger.info("Email sent!")
