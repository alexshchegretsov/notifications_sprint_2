import os

from aiohttp import web
from app import app

port = os.getenv('API_APP_PORT', 9999)

web.run_app(app, host='0.0.0.0', port=port,
            access_log_format='%a %t "%r" %s %b %Tf "%{Referer}i" "%{User-Agent}i"')
