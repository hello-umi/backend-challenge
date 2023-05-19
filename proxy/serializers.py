from rest_framework import serializers

from proxy.models import Message, Topic

from .tasks import process_message


class TopicSerializer(serializers.ModelSerializer):
    """Topic Serializer used to Retrieve or Create Topics"""

    @classmethod
    def get_queryset(cls):
        return Topic.objects.all()

    def validate_channel(self, value):
        """Ensures a valid channel argument was passed"""
        if value in Topic.get_available_channels():
            return value
        raise serializers.ValidationError("Not a valid Channel!")

    class Meta:
        model = Topic
        fields = ["id", "name", "channel"]


class MessageSerializer(serializers.ModelSerializer):
    """Message Serializer used to Retrieve or Create Topics"""

    topic = serializers.CharField(source="topic.name", required=True)

    @classmethod
    def get_queryset(cls):
        return Message.objects.all()

    def validate_topic(self, value):
        """Ensures the topic passed as argument is a valid one"""
        try:
            Topic.objects.get(name__iexact=value)
            return value
        except Topic.DoesNotExist:
            raise serializers.ValidationError("Not a valid Topic!")

    def create(self, validated_data):
        """Creates the message and enqueues it"""

        topic_name = validated_data.pop("topic")["name"]
        topic = Topic.objects.get(name=topic_name)
        validated_data["topic"] = topic
        message = Message.objects.create(**validated_data)
        process_message.delay(message.id)

        return message

    class Meta:
        model = Message
        fields = ["id", "description", "dt_created", "dt_updated", "status", "topic"]
