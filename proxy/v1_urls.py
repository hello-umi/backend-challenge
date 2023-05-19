from django.urls import path

from . import views

urlpatterns = [
    path("status", views.status, name="status"),
    path("messages/", views.MessageListCreateAPIView.as_view(), name="message-list"),
    path("messages/<int:pk>/", views.MessageDetailAPIView.as_view(), name="message-detail"),
    path("topics/", views.TopicListCreateAPIView.as_view(), name="topic-list"),
    path("topics/<int:pk>/", views.TopicDetailAPIView.as_view(), name="topic-detail"),
]
