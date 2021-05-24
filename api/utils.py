from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import text

from settings import SQLALCHEMY_DATABASE_URI, AUTH_DB_URL


def init_db(expire_on_commit=False):
    engine = create_engine(url=SQLALCHEMY_DATABASE_URI)
    db = scoped_session(sessionmaker(bind=engine, expire_on_commit=expire_on_commit))
    return db


def auth_db():
    return create_engine(url=AUTH_DB_URL)


def get_email_by_user_id(user_id):
    engine = auth_db()

    with engine.connect() as conn:
        res = conn.execute(text('select email from users where id = :user_id'), {'user_id': user_id})
        email = res.fetchone()[0]
    return email
