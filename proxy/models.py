from django.db import models

from proxy.strategies.strategy_registry import CHANNEL_STRATEGY_REGISTRY


class Topic(models.Model):
    name = models.CharField(max_length=200)

    channel_choices = [(key, key.title())for key in CHANNEL_STRATEGY_REGISTRY.keys()]
    channel = models.CharField(max_length=200, choices=channel_choices)

    def get_channel(self):
        return CHANNEL_STRATEGY_REGISTRY.get(self.channel)

    @classmethod
    def get_available_channels(cls):
        return [channel[0] for channel in cls.channel_choices]


class Message(models.Model):
    PENDING = 1
    QUEUED = 2
    ERROR = 3
    SENT = 4

    description = models.TextField()
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)
    status_codes = ((PENDING, "PENDING"), (QUEUED, "QUEUED"), (ERROR, "ERROR"), (SENT, "SENT"))
    status = models.IntegerField(choices=status_codes, default=1)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)

    def set_status(self, status_code):
        self.status = status_code
        self.save()

    def get_channel(self):
        return self.topic.get_channel()

    def format_body(self):
        return f"Topic: {self.topic.name}, Message: {self.description}"
