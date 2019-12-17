from django.contrib.auth.models import AnonymousUser

import pytest

from {{ cookiecutter.project_slug }}.apps.accounts.api.permissions import IsNotAuthenticated


def test_is_not_authenticated_permission_true(mocker):
    request = mocker.MagicMock()
    view = mocker.MagicMock()
    request.user = AnonymousUser()

    permission = IsNotAuthenticated()
    assert permission.has_permission(request, view)


@pytest.mark.django_db
def test_is_not_authenticated_permission_false(user_account, mocker):
    request = mocker.MagicMock()
    view = mocker.MagicMock()
    request.user = user_account()

    permission = IsNotAuthenticated()
    assert not permission.has_permission(request, view)
