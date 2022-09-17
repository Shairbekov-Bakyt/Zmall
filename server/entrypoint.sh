#!/bin/bash

# Collect static files
echo "Collect static files"
python3 manage.py collectstatic --no-input

# migrate
echo "migrate"
python3 manage.py migrate --settings config.settings.production

# Start server
echo "Starting server"

#python3 manage.py runserver 0.0.0.0:8000
gunicorn --env DJANGO_SETTINGS_MODULE=config.settings.production config.wsgi:application --bind 0.0.0.0:8000
#gunicorn config.wsgi

exec "$@"
