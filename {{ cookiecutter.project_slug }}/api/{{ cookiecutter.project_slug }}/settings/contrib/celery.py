from ..django import TIME_ZONE as DJANGO_TIME_ZONE
from ..environment import env


CELERY_TASK_ALWAYS_EAGER = env.bool(
    "{{ cookiecutter.project_slug | upper() }}_CELERY_TASK_ALWAYS_EAGER", default=False
)
CELERY_BROKER_URL = env.str(
    "{{ cookiecutter.project_slug | upper() }}_CELERY_BROKER",
    default="redis://redis:6379/1",
)

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = DJANGO_TIME_ZONE

CELERYBEAT_SCHEDULE = {}
