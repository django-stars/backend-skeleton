import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration

from {{ cookiecutter.project_slug }}.settings.environment import env


USE_SENTRY = env.bool("{{ cookiecutter.__env_prefix }}USE_SENTRY", default=True)
if USE_SENTRY:  # pragma: no cover
    sentry_kwargs = {
        "dsn": env.str("{{ cookiecutter.__env_prefix }}SENTRY_DSN"),
        "environment": env.str("{{ cookiecutter.__env_prefix }}SENTRY_ENVIRONMENT"),
        "integrations": [DjangoIntegration()],
    }
    sentry_sdk.init(**sentry_kwargs)  # pylint: disable=abstract-class-instantiated
