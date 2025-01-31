from ..environment import env


AWS_S3_ACCESS_KEY_ID = env.str("AWS_S3_ACCESS_KEY_ID")
AWS_S3_SECRET_ACCESS_KEY = env.str("AWS_S3_SECRET_ACCESS_KEY")
AWS_S3_ENDPOINT_URL = env.str("{{ cookiecutter.__env_prefix }}DEFAULT_FILE_STORAGE_ENDPOINT_URL")
AWS_STORAGE_BUCKET_NAME = env.str("{{ cookiecutter.__env_prefix }}DEFAULT_FILE_STORAGE_BUCKET_NAME")


DEFAULT_FILE_STORAGE_BACKEND = env.str(
    "{{ cookiecutter.__env_prefix }}DEFAULT_FILE_STORAGE_BACKEND", default="storages.backends.s3boto3.S3Boto3Storage"
)
DEFAULT_FILE_STORAGE_OPTIONS = {}
if DEFAULT_FILE_STORAGE_BACKEND == "storages.backends.s3boto3.S3Boto3Storage":
    DEFAULT_FILE_STORAGE_OPTIONS = {
        "bucket_name": env.str("{{ cookiecutter.__env_prefix }}DEFAULT_FILE_STORAGE_BUCKET_NAME"),
        "endpoint_url": env.str("{{ cookiecutter.__env_prefix }}DEFAULT_FILE_STORAGE_ENDPOINT_URL"),
        "custom_domain": env.str("{{ cookiecutter.__env_prefix }}DEFAULT_FILE_STORAGE_CUSTOM_DOMAIN"),
        "url_protocol": env.str("{{ cookiecutter.__env_prefix }}DEFAULT_FILE_STORAGE_URL_PROTOCOL", default="https:"),
        "location": env.str("{{ cookiecutter.__env_prefix }}DEFAULT_FILE_STORAGE_LOCATION", default="m"),
        "file_overwrite": env.bool("{{ cookiecutter.__env_prefix }}DEFAULT_FILE_STORAGE_FILE_OVERWRITE", default=False),
    }

STATICFILES_STORAGE_BACKEND = env.str(
    "{{ cookiecutter.__env_prefix }}STATICFILES_STORAGE_BACKEND", default="storages.backends.s3boto3.S3StaticStorage"
)
STATICFILES_STORAGE_OPTIONS = {}
if STATICFILES_STORAGE_BACKEND == "storages.backends.s3boto3.S3StaticStorage":
    STATICFILES_STORAGE_OPTIONS = {
        "bucket_name": env.str("{{ cookiecutter.__env_prefix }}DEFAULT_FILE_STORAGE_BUCKET_NAME"),
        "endpoint_url": env.str("{{ cookiecutter.__env_prefix }}DEFAULT_FILE_STORAGE_ENDPOINT_URL"),
        "custom_domain": env.str("{{ cookiecutter.__env_prefix }}DEFAULT_FILE_STORAGE_CUSTOM_DOMAIN"),
        "url_protocol": env.str("{{ cookiecutter.__env_prefix }}DEFAULT_FILE_STORAGE_URL_PROTOCOL", default="https:"),
        "location": env.str("{{ cookiecutter.__env_prefix }}STATICFILES_STORAGE_LOCATION", default="s"),
        "file_overwrite": env.bool("{{ cookiecutter.__env_prefix }}STATICFILES_STORAGE_FILE_OVERWRITE", default=True),
    }


STORAGES = {
    "default": {
        "BACKEND": DEFAULT_FILE_STORAGE_BACKEND,
        "OPTIONS": DEFAULT_FILE_STORAGE_OPTIONS,
    },
    "staticfiles": {
        "BACKEND": STATICFILES_STORAGE_BACKEND,
        "OPTIONS": STATICFILES_STORAGE_OPTIONS,
    },
}
