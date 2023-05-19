from pathlib import Path

bind = "0.0.0.0:8000"  # Replace with your desired host and port
workers = 4  # Adjust the number of workers based on your requirements
errorlog = "-"  # Send error logs to stdout
accesslog = "-"  # Send access logs to stdout
capture_output = True  # Capture stdout/stderr in the logs

# Define the location of the static files
static_path = str(Path(__file__).resolve().parent / "static")


# Create an application that serves both your Django app and the static files
def create_app():
    from django.core.wsgi import get_wsgi_application
    from whitenoise import WhiteNoise

    # Get the Django application
    django_app = get_wsgi_application()

    # Create a WhiteNoise application to serve the static files
    static_app = WhiteNoise(django_app, root=static_path)

    return static_app


# Define the Gunicorn application
application = create_app()
