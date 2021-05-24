import logging

from config.celery import app
from admin_panel.models import Notification

logger = logging.getLogger(__name__)


@app.task(autoretry_for=(Exception, ), retry_backoff=True)
def email(**kwargs):
    notify_id = kwargs.get('notify_id')
    data = kwargs.get('data')

    notification = Notification.objects.get(pk=notify_id)
    notification.do_notify(data=data)
    notification.save()
