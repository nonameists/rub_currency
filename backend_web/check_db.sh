#!/bin/bash

while ! nc -z db 5432; do
  echo "Waiting for the database to be available..."
  sleep 1
done

python manage.py migrate
python manage.py migrate django_celery_beat
python manage.py collectstatic --noinput
gunicorn backend.wsgi:application --bind 0.0.0.0:8000