#!/usr/bin/env bash

echo "Start worker beat..."
celery -A config beat -S django
echo "Worker started"