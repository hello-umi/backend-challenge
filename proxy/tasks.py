import logging

from celery import shared_task

from proxy.message_sender import MessageSender

logger = logging.getLogger(__name__)


@shared_task
def process_message(message_id):
    """Async Taks that takes the message ID and sends that message with the correct strategy"""
    try:
        logger.info("Task received to process message_id:%d", message_id)
        sender = MessageSender(message_id)
        sender.send_message()
        logger.info("Task completed for message_id:%d", message_id)
    except Exception:
        logger.exception("There was an error processing message_id:%d", message_id)
