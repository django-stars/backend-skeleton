from {{ cookiecutter.project_slug }}.settings.environment import env


REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_AUTHENTICATION_CLASSES": ("{{ cookiecutter.project_slug }}.apps.accounts.api.authentication.CustomSessionAuthentication",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
    "DEFAULT_RENDERER_CLASSES": env.tuple(
        "{{ cookiecutter.__env_prefix }}DEFAULT_RENDERER_CLASSES", default=("rest_framework.renderers.JSONRenderer",)
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "PAGE_SIZE": 100,
}
