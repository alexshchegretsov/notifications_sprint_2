import os
from logging import config as logging_config

import jinja2

logging_config.fileConfig('logging.ini')
NOTIFY_LOGGER_NAME = 'notifyApiLogger'

JWT_ALGORITHM = 'RS256'
PUBLIC_KEY = os.getenvb(b'PUBLIC_KEY')

DEFAULT_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'x-request-id, content-type, x-csrftoken',
    'Access-Control-Allow-Methods': 'GET, PUT, DELETE, OPTIONS, POST',
    'Content-Type': 'application/json',
    'Connection': 'Keep-Alive'
}

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@localhost:5432/notify'

TEMPLATE_ROOT = os.path.join(os.path.dirname(__file__), 'templates')
jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_ROOT),
                                autoescape=False,
                                extensions=['jinja2.ext.i18n'])

SSL_PORT = 465  # For SSL
SMTP_SERVER = 'smtp.gmail.com'
SENDER_EMAIL = 'notifysmtp2@gmail.com'
SENDER_PASSWORD = 'notifysmtp12345'

AUTH_DB_URL = 'postgresql+psycopg2://postgres:postgres@84.201.181.184:5432/auth'
