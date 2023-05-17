from rest_framework import serializers

from proxy.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "body", "dt_created", "dt_updated", "status"]
