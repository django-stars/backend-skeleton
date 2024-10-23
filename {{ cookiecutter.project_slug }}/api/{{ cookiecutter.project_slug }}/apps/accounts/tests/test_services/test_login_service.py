import pytest

from pytest_mock import MockerFixture
from rest_framework import status

from django.test.client import RequestFactory
from django.urls import reverse

from {{ cookiecutter.project_slug }}.apps.accounts.services.login import LoginService
from {{ cookiecutter.project_slug }}.fixtures.user_account import UserAccountMaker


@pytest.mark.django_db
def test_login_service_login(user_account: UserAccountMaker, mocker: MockerFixture) -> None:
    request = mocker.MagicMock()
    user = user_account()
    service = LoginService
    mocked_django_login = mocker.patch.object(service, "_django_login")

    response = service.login(request, user)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    mocked_django_login.assert_called_once_with(request, user)


def test_login_service_logout(user_account: UserAccountMaker, mocker: MockerFixture) -> None:
    user = user_account()
    request = RequestFactory().post(reverse("api-v1-accounts:logout"))
    request.user = user
    service = LoginService
    mocked_django_logout = mocker.patch.object(service, "_django_logout")

    response = service.logout(request)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    mocked_django_logout.assert_called_once_with(request)
