from rest_framework import serializers

from proxy.models import Message, Topic
from .strategies.strategy_registry import CHANNEL_STRATEGY_REGISTRY

from .tasks import process_message


class TopicSerializer(serializers.ModelSerializer):

    @classmethod
    def get_queryset(cls):
        return Topic.objects.all()

    def validate_channel(self, value):
        if value in Topic.get_available_channels():
            return value
        raise serializers.ValidationError("Not a valid Channel!")

    class Meta:
        model = Topic
        fields = ["id", "name", "channel"]


class MessageSerializer(serializers.ModelSerializer):
    topic = serializers.CharField(source="topic.name", required=True)

    @classmethod
    def get_queryset(cls):
        return Message.objects.all()

    def validate_topic(self, value):
        try:
            Topic.objects.get(name__iexact=value)
            return value
        except Topic.DoesNotExist:
            raise serializers.ValidationError("Not a valid Topic!")

    def create(self, validated_data):
        topic_name = validated_data.pop("topic")["name"]
        topic = Topic.objects.get(name=topic_name)
        validated_data["topic"] = topic
        message = Message.objects.create(**validated_data)
        process_message.delay(message.id)

        return message

    class Meta:
        model = Message
        fields = ["id", "description", "dt_created", "dt_updated", "status", "topic"]
