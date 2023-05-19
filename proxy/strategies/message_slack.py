from proxy.strategies.message_strategy import MessagingStrategy
import logging

logger = logging.getLogger(__name__)


class SlackMessagingStrategy(MessagingStrategy):
    def send_message(self, message):
        logger.info(f"Sending Slack message: {message}")
