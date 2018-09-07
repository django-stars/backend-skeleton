from celery.schedules import crontab  # noqa

from .environment import env  # noqa


CELERY_TASK_ALWAYS_EAGER = env.bool('CELERY_TASK_ALWAYS_EAGER', default=False)

CELERY_ACCEPT_CONTENT = ['application/x-python-serialize']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = env.str('TIME_ZONE', default='UTC')

CELERYBEAT_SCHEDULE = {
}
