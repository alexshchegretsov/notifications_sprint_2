#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z $PG_HOST $PG_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Migrate apply..."
alembic upgrade head

echo "start api service..."
python3 async_api.py --port $PORT