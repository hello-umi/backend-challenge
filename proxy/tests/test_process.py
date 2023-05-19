from unittest import mock

from model_bakery import baker

from django.test import TestCase

from proxy.message_sender import MessageSender
from proxy.models import Message, Topic
from proxy.strategies.message_email import EmailMessagingStrategy
from proxy.strategies.message_slack import SlackMessagingStrategy


class ProcessingMessagesTestCase(TestCase):

    def test_processing_messages_task_slack(self):
        topic = baker.make(Topic, channel="slack")
        message = baker.make(Message, status=1, topic=topic)
        sender = MessageSender(message.id)
        self.assertIsNotNone(sender)
        self.assertTrue(topic.get_channel(), SlackMessagingStrategy)
        sender.send_message()
        message.refresh_from_db()
        self.assertEqual(message.status, 4)

    def test_processing_messages_task_invalid_channel(self):
        topic = baker.make(Topic, channel="invalid")
        message = baker.make(Message, status=1, topic=topic)
        sender = MessageSender(message.id)
        self.assertIsNotNone(sender)
        self.assertIsNone(topic.get_channel())
        sender.send_message()
        message.refresh_from_db()
        self.assertEqual(message.status, 3)

    def test_processing_messages_task_email_missing_env(self):
        topic = baker.make(Topic, channel="email")
        message = baker.make(Message, status=1, topic=topic)
        sender = MessageSender(message.id)
        sender.send_message()
        message.refresh_from_db()
        self.assertEqual(message.status, 3)

    @mock.patch("os.getenv")
    @mock.patch("proxy.strategies.message_email.send_mail")
    def test_processing_messages_task_email(self, mocked_mail, mocked_get_env):
        mocked_get_env.return_value = "SOME_VALUE"
        topic = baker.make(Topic, channel="email")
        message = baker.make(Message, status=1, topic=topic)
        sender = MessageSender(message.id)
        self.assertIsNotNone(sender)
        self.assertTrue(topic.get_channel(), EmailMessagingStrategy)
        sender.send_message()
        message.refresh_from_db()
        self.assertEqual(message.status, 4)
        mocked_mail.assert_called_once_with("SOME_VALUE", message.format_body(), "SOME_VALUE", ["SOME_VALUE"])
