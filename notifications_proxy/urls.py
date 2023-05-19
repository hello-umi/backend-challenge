"""
URL configuration for notifications_proxy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Notifications Proxy API",
        default_version="v1",
        description="Backend Challenge by Diego Santos",
        contact=openapi.Contact(email="diesantosg@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path("v1/", include("proxy.v1_urls")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
