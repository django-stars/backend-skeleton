import pytest

from {{ cookiecutter.project_slug }}.apps.accounts.models import UserAccount
from {{ cookiecutter.project_slug }}.apps.accounts.selectors import get_all_users


@pytest.mark.django_db
def test_get_all_user_selector(user_account):
    assert UserAccount.objects.count() == 0
    user_account(_quantity=3)
    assert UserAccount.objects.filter(is_active=True).count() == 3
    queryset = get_all_users()
    assert queryset.count() == 3
