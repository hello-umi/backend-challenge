#!/bin/sh
export DJANGO_SETTINGS_MODULE=notifications_proxy.settings.settings

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying database creation and migrations..."
python manage.py init_postgres

exec "$@"
