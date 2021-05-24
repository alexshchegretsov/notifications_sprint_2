import logging

from django.db import OperationalError

from config.celery import app
from admin_panel.utils import get_emails_by_timezone
from admin_panel.tasks.email import email
from admin_panel.models import Notification, Content

logger = logging.getLogger(__file__)


@app.task(autoretry_for=(OperationalError, ), retry_backoff=True)
def weekly_movies_by_tz(tz: int, event: str):
    emails = get_emails_by_timezone(tz=tz)
    content = Content.objects.filter(event=event).first()
    data = ' '.join(['new_film_1', 'new_film_2'])

    for e in emails:
        n = Notification.objects.create(content_id=content, recipient=e)
        email.delay(notify_id=n.id_as_str, data=data)


@app.task
def weekly_fresh_movies_runner():
    event = 'weekly_movies'
    # for test
    # weekly_movies_by_tz.apply_async(args=(0, event), countdown=0 * 60 * 60)
    for i in range(24):
        weekly_movies_by_tz.apply_async(args=(i, event), countdown=i * 60 * 60)
