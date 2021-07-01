import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration

from ..environment import env


USE_SENTRY = env.bool("{{ cookiecutter.project_slug | upper() }}_USE_SENTRY", default=True)
if USE_SENTRY:  # pragma: no cover
    sentry_kwargs = {
        "dsn": env.str("{{ cookiecutter.project_slug | upper() }}_SENTRY_DSN"),
        "environment": env.str("{{ cookiecutter.project_slug | upper() }}_SENTRY_ENVIRONMENT"),
        "integrations": [DjangoIntegration()],
    }
    sentry_sdk.init(**sentry_kwargs)  # pylint: disable=abstract-class-instantiated
