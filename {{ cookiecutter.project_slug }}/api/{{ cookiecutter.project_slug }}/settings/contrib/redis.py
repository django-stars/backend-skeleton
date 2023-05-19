from ..environment import env


REDIS_URL = env.str("{{ cookiecutter.__env_prefix }}REDIS_URL", default="redis://redis:6379/2")
