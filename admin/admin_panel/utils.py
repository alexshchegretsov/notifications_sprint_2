from sqlalchemy import create_engine
from sqlalchemy.sql import text

from django.conf import settings


def auth_db():
    return create_engine(url=settings.AUTH_DB_URL)


def get_emails_by_timezone(tz: int):
    engine = auth_db()

    with engine.connect() as conn:
        res = conn.execute(text('select email from users where tz = :tz and notify = true'), {'tz': tz})
        res = res.fetchall()
        res = [x[0] for x in res]
    return res
