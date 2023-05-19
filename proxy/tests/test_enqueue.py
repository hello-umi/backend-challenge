from unittest import mock

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from proxy.models import Message


class MessageEnqueueTestCase(TestCase):
    """Test Case for creation of messages and ensure they are enqueued"""

    def setUp(self):
        self.client = APIClient()

    @mock.patch("proxy.serializers.process_message.delay")
    def test_messages_are_created_and_enqueued(self, mocked_process_delay):
        data = {"description": "Test description", "topic": "Sales"}
        response = self.client.post("/messages/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        message_id = response.data.get("id")
        message = Message.objects.get(id=message_id)
        self.assertEqual(message.description, data["description"])
        mocked_process_delay.assert_called_once_with(message.id)

    @mock.patch("proxy.serializers.process_message.delay")
    def test_messages_are_not_created_and_not_enqueued(self, mocked_process_delay):
        data = {"description": "Test description", "topic": "XXXXX"}
        response = self.client.post("/messages/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        with self.assertRaises(KeyError):
            _ = response.data["id"]
        mocked_process_delay.assert_not_called()
