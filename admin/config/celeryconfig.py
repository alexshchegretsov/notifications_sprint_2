import os
from kombu import Exchange, Queue

broker_url = f'amqp://{os.getenv("RMQ_USER", "guest")}:{os.getenv("RMQ_PASSWORD", "")}@' \
             f'{os.getenv("RMQ_HOST", "localhost")}:{os.getenv("RMQ_PORT", "5672")}/{os.getenv("RMQ_VHOST", "/")}'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True

task_acks_late = True
default_queue_name = 'default'
default_exchange_name = 'default'
default_routing_key = 'default'
default_exchange = Exchange(default_exchange_name, type='direct')
task_queues = (
    Queue('weekly_movie_runner', default_exchange, routing_key='weekly_movie_runner'),
    Queue('weekly_movie', default_exchange, routing_key='weekly_movie'),
    Queue('sales_off', default_exchange, routing_key='sales_off'),
    Queue('email_admin', default_exchange, routing_key='notify_email_admin')
)
task_routes = {
    'admin_panel.tasks.base.weekly_movies_by_tz': {'queue': 'weekly_movie', 'routing_key': 'weekly_movie'},
    'admin_panel.tasks.base.weekly_fresh_movies_runner': {'queue': 'weekly_movie_runner', 'routing_key': 'weekly_movie_runner'},
    'admin_panel.tasks.email.email': {'queue': 'email_admin', 'routing_key': 'notify_email_admin'},
}
task_default_queue = default_queue_name
task_default_exchange = default_exchange_name
task_default_routing_key = default_routing_key
