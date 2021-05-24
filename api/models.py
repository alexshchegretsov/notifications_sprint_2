import uuid
import datetime as dt

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, ForeignKey, String, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from settings import jinja2_env
from misc import EmailSender

Base = declarative_base()
metadata = Base.metadata


class Content(Base):
    __tablename__ = 'content'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    event = Column(String, nullable=False)
    text = Column(Text)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    def __str__(self):
        return self.text[:50]


class Notification(Base):
    __tablename__ = 'notification'

    sender = EmailSender
    STATUS_PENDING = 'pending'
    STATUS_DONE = 'done'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    content_id = Column(UUID(as_uuid=True), ForeignKey('content.id'), nullable=False)
    content = relationship('Content')
    event = association_proxy('content', 'event')
    content_text = association_proxy('content', 'text')
    recipient = Column(String, nullable=False)
    status = Column(String, default=STATUS_PENDING, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    @property
    def id_as_str(self):
        return str(self.id)

    def do_notify(self, data=None):
        html_data = self._get_html(data=data)
        self.sender.send(html=html_data, subject=self.event, receiver_email=self.recipient)
        self._notify_done()

    def _notify_done(self):
        self.status = self.STATUS_DONE

    def _get_html(self, data=None):
        ctx = {'content': self.content_text}
        if data:
            ctx['data'] = data
        template = jinja2_env.get_template(f'{self.event}.html')
        return template.render(ctx)


class Compaigne(Base):
    __tablename__ = 'compaigne'

    id = Column(Integer, primary_key=True)
    content_id = Column(UUID(as_uuid=True), ForeignKey('content.id'), nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
