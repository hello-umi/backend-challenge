import logging

from proxy.strategies.message_strategy import MessagingStrategy

logger = logging.getLogger(__name__)


class SlackMessagingStrategy(MessagingStrategy):
    """Mocked implementation of Slack Integration"""

    def send_message(self, message):
        logger.info(f"Sending Slack message: {message}")
