from django.urls import path

from . import views

urlpatterns = [
    path("status", views.status, name="status"),
    path("messages/", views.message_list),
    path("messages/<int:pk>/", views.message_detail),
]
