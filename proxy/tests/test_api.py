from unittest import mock

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class MessageAPITestCase(TestCase):
    """Basic HTTP REST methods tests for Messages"""

    def setUp(self):
        self.client = APIClient()

    def test_get_messages(self):
        response = self.client.get("/messages/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @mock.patch("proxy.serializers.process_message")
    def test_create_message_with_valid_data(self, _):
        data = {"description": "Test description", "topic": "Sales"}
        response = self.client.post("/messages/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @mock.patch("proxy.serializers.process_message")
    def test_create_message_with_invalid_data1(self, _):
        data = {"something": "Test description", "topic": "Sales"}
        response = self.client.post("/messages/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch("proxy.serializers.process_message")
    def test_create_message_with_invalid_data2(self, _):
        data = {"description": "Test description", "something": "Sales"}
        response = self.client.post("/messages/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch("proxy.serializers.process_message")
    def test_create_message_with_invalid_topic(self, _):
        data = {"description": "Test description", "topic": "Invalid Topic"}
        response = self.client.post("/messages/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TopicAPITestCase(TestCase):
    """Basic HTTP REST methods tests for Topics"""

    def setUp(self):
        self.client = APIClient()

    def test_get_topics(self):
        response = self.client.get("/topics/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_topic_with_valid_data(self):
        data = {"name": "Test name", "channel": "email"}
        response = self.client.post("/topics/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_topic_with_invalid_data1(self):
        data = {"xxx": "Test name", "channel": "email"}
        response = self.client.post("/topics/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_topic_with_invalid_data2(self):
        data = {"name": "Test name", "yyyy": "email"}
        response = self.client.post("/topics/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_topic_with_invalid_topic(self):
        data = {"name": "Test name", "channel": "aaaaa"}
        response = self.client.post("/topics/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
