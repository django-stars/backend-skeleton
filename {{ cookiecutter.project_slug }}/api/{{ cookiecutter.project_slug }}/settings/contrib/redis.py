from ..environment import env


REDIS_URL = env.str(
    "{{ cookiecutter.project_slug | upper() }}_REDIS_URL",
    default="redis://redis:6379/2",
)
