from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView
from proxy.serializers import MessageSerializer, TopicSerializer


def status(request):
    return HttpResponse("OK")


class MessageListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of messages or create new
    """

    serializer_class = MessageSerializer
    queryset = MessageSerializer.get_queryset()


class MessageDetailAPIView(RetrieveAPIView):
    """
    API view to retrieve a specific message
    """

    queryset = MessageSerializer.get_queryset()
    serializer_class = MessageSerializer


class TopicListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of Topics or create new
    """

    serializer_class = TopicSerializer
    queryset = TopicSerializer.get_queryset()


class TopicDetailAPIView(RetrieveAPIView):
    """
    API view to retrieve a specific Topic
    """

    queryset = TopicSerializer.get_queryset()
    serializer_class = TopicSerializer



