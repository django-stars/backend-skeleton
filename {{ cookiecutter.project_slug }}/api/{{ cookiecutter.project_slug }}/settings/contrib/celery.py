from ..environment import env


CELERY_TASK_ALWAYS_EAGER = env.bool("{{ cookiecutter.__env_prefix }}CELERY_TASK_ALWAYS_EAGER", default=False)
CELERY_BROKER_URL = env.str("{{ cookiecutter.__env_prefix }}CELERY_BROKER", default="redis://redis:6379/1")

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = env.str("{{ cookiecutter.__env_prefix }}TIME_ZONE", default="UTC")

CELERYBEAT_SCHEDULE = {}
