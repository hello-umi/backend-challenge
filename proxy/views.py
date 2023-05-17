from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from proxy.models import Message
from proxy.serializers import MessageSerializer


def status(request):
    return HttpResponse("OK")


@csrf_exempt
def message_list(request):
    """
    List latest's messages, or create a new message.
    """
    if request.method == "GET":
        messages = Message.objects.all().order_by("-dt_created")[:50]
        serializer = MessageSerializer(messages, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def message_detail(request, pk):
    """
    Retrieve a message.
    """
    try:
        message = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = MessageSerializer(message)
        return JsonResponse(serializer.data)
