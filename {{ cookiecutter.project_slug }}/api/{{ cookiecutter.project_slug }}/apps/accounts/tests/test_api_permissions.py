import pytest

from pytest_mock import MockerFixture

from django.contrib.auth.models import AnonymousUser

from {{ cookiecutter.project_slug }}.apps.accounts.api.permissions import IsNotAuthenticated
from {{ cookiecutter.project_slug }}.fixtures.user_account import UserAccountMaker


def test_is_not_authenticated_permission_true(mocker: MockerFixture) -> None:
    request = mocker.MagicMock()
    view = mocker.MagicMock()
    request.user = AnonymousUser()

    permission = IsNotAuthenticated()
    assert permission.has_permission(request, view)


@pytest.mark.django_db
def test_is_not_authenticated_permission_false(user_account: UserAccountMaker, mocker: MockerFixture) -> None:
    request = mocker.MagicMock()
    view = mocker.MagicMock()
    request.user = user_account()

    permission = IsNotAuthenticated()
    assert not permission.has_permission(request, view)
