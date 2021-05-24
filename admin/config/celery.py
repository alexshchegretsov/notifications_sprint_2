import os

from celery import Celery
from kombu import Exchange, Queue

# set the default Django settings module for the 'celery' program.
env_settings = os.getenv("CONFIG_ENV", "config.settings.dev")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', env_settings)

app = Celery('notify')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object(f'django.conf:settings', namespace='CELERY')
app.config_from_object('config.celeryconfig', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
