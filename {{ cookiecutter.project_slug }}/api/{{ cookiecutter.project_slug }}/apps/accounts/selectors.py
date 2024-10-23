from django.db.models import QuerySet

from {{ cookiecutter.project_slug }}.apps.accounts.models import UserAccount


def get_all_users() -> QuerySet[UserAccount]:
    return UserAccount.objects.active()
