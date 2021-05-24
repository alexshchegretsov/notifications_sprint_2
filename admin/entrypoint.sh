#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z $PG_HOST $PG_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Collect static..."
python manage.py collectstatic --noinput

sleep 5

echo "Migrate apply..."
python manage.py migrate admin_panel 0001 --fake

echo "start gunicorn..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000