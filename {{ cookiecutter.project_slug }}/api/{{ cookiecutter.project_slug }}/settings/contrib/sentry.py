import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration

from ..environment import env


USE_SENTRY = env.bool("{{ cookiecutter.env_prefix }}USE_SENTRY", default=True)
if USE_SENTRY:  # pragma: no cover
    sentry_kwargs = {
        "in_app_include": ["{{ cookiecutter.project_slug }}"],
        "dsn": env.str("{{ cookiecutter.env_prefix }}SENTRY_DSN"),
        "environment": env.str("{{ cookiecutter.env_prefix }}SENTRY_ENVIRONMENT"),
        "integrations": [DjangoIntegration()],
    }
    sentry_sdk.init(**sentry_kwargs)  # pylint: disable=abstract-class-instantiated
