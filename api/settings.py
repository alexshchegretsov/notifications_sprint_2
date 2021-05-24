import os
from logging import config as logging_config

from jinja2 import Environment, FileSystemLoader

logging_config.fileConfig('logging.ini')
NOTIFY_LOGGER_NAME = 'notifyApiLogger'

DEFAULT_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'x-request-id, content-type, x-csrftoken',
    'Access-Control-Allow-Methods': 'GET, PUT, DELETE, OPTIONS, POST',
    'Content-Type': 'application/json',
    'Connection': 'Keep-Alive'
}

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', '')
AUTH_DB_URL = os.getenv('AUTH_DB_URL', '')

TEMPLATE_ROOT = os.path.join(os.path.dirname(__file__), 'templates')
jinja2_env = Environment(
    loader=FileSystemLoader(TEMPLATE_ROOT),
    autoescape=True,
    extensions=['jinja2.ext.i18n'],
)

SSL_PORT = os.getenv('SMTP_SSL_PORT', 465)
SMTP_SERVER = os.getenv('SMTP_SERVER', '')
SENDER_EMAIL = os.getenv('SENDER_EMAIL', '')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', '')
