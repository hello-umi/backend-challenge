import logging

from proxy.models import Message

logger = logging.getLogger(__name__)


class MessageSender(object):
    """Actual Message Dispatcher"""

    def __init__(self, message_id):
        self.message_id = message_id
        self.message = Message.objects.get(id=message_id)

    def send_message(self):
        """Sends the message with the correct channel and strategy"""
        strategy = self.message.get_channel()
        logger.info("Sending message with strategy %s", strategy)
        try:
            strategy().send_message(self.message.format_body())
            self.message.set_status(Message.SENT)
        except Exception as e:
            logger.exception(
                "Something went wrong sending message %d with strategy %s",
                self.message_id,
                strategy,
            )
            self.message.set_status(Message.ERROR)
