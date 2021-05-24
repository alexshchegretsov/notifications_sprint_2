import logging

import dramatiq

from settings import NOTIFY_LOGGER_NAME
from utils import init_db, get_email_by_user_id
from models import Notification, Content

logger = logging.getLogger(NOTIFY_LOGGER_NAME)


@dramatiq.actor(queue_name='api_email', priority=20)
def email(**kwargs):
    notify_id = kwargs.get('notify_id')
    outer_data = kwargs.get('data')
    session = init_db()
    notification = session.query(Notification).filter(Notification.id == notify_id).scalar()
    try:
        notification.do_notify(data=outer_data)
    except Exception as err:
        logger.error(err)
        session.close()
        raise

    session.commit()
    session.close()


@dramatiq.actor(queue_name='api_prepare_register_user', priority=10)
def prepare_register_user(data):
    session = init_db()
    event = data.get('event')
    email = data.get('email')
    content_id = session.query(Content.id).filter(Content.event == event).scalar()
    logger.info(f'content id is {content_id}')
    notification = Notification(content_id=content_id, recipient=email)
    session.add(notification)
    session.commit()

    for queue in event_send_queues_mapper.get(event):
        queue.send(notify_id=notification.id_as_str)

    session.close()


@dramatiq.actor(queue_name='api_prepare_comment_like', priority=10)
def prepare_comment_like(data):
    session = init_db()
    event = data.get('event')
    outer_data = data.get('data')
    user_id = data.get('user_id')

    email = get_email_by_user_id(user_id)
    content_id = session.query(Content.id).filter(Content.event == event).scalar()
    notification = Notification(content_id=content_id, recipient=email)
    session.add(notification)
    session.commit()

    for queue in event_send_queues_mapper.get(event):
        queue.send(notify_id=notification.id_as_str, data=outer_data)

    session.close()


event_prepare_queues_mapper = {
    'register_user': prepare_register_user,
    'comment_like': prepare_comment_like
}

event_send_queues_mapper = {
    'register_user': [email],
    'comment_like': [email],
}


@dramatiq.actor(queue_name='api_sort', priority=0)
def sort(data):
    event = data.get('event')
    queue = event_prepare_queues_mapper.get(event)
    queue.send(data)
