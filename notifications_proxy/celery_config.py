from celery import Celery
from django.conf import settings

# Initialize Celery app
app = Celery("notifications_proxy")

# Load Celery settings from Django settings
app.config_from_object(settings, namespace="CELERY")

# Set up the Celery autodiscover mechanism
app.autodiscover_tasks()
