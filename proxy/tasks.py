import logging

from celery import shared_task

from proxy.message_sender import MessageSender

logger = logging.getLogger(__name__)


@shared_task
def process_message(message_id):
    try:
        logger.info(f"Task received to process message_id:{message_id}")
        sender = MessageSender(message_id)
        sender.send_message()
        logger.info(f"Task completed for message_id:{message_id}")
    except Exception:
        logger.exception(f"There was an error processing message_id:{message_id}")
