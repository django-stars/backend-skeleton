import logging

from {{ cookiecutter.project_slug }} import celery_app
from {{ cookiecutter.project_slug }}.apps.accounts.services.notifications import notification


logger = logging.getLogger(__name__)


@celery_app.task
def send_notification(user_email: str, kind: str, context: dict):
    logger.debug(f"Sending {kind} notification to user {user_email}")

    notification(user_email, kind, context)
