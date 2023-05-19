import logging

from proxy.models import Message

logger = logging.getLogger(__name__)


class MessageSender(object):
    def __init__(self, message_id):
        self.message_id = message_id
        self.message = Message.objects.get(id=message_id)

    def send_message(self):
        strategy = self.message.get_channel()
        logger.info(f"Sending message with strategy {strategy}")
        try:
            strategy().send_message(self.message.format_body())
            self.message.set_status(Message.SENT)
        except Exception as e:
            logger.info(f"Something went wrong sending message {self.message_id} with strategy {strategy}")
            self.message.set_status(Message.ERROR)

