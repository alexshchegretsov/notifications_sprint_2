"""
WSGI config for notify project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

env_settings = os.getenv("CONFIG_ENV", "config.settings.dev")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', env_settings)

application = get_wsgi_application()
