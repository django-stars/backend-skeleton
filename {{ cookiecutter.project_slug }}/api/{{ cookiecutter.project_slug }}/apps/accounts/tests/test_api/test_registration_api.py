import pytest

from pytest_mock import MockerFixture
from rest_framework import status
from rest_framework.response import Response

from django.urls import reverse

from {{ cookiecutter.project_slug }}.apps.accounts.models import UserAccount
from {{ cookiecutter.project_slug }}.fixtures.api_client import CustomAPIClient


@pytest.mark.django_db
def test_registration_api_success(unauthorized_api_client: CustomAPIClient, mocker: MockerFixture) -> None:
    assert not UserAccount.objects.exists()
    mocked_response = Response(status=status.HTTP_204_NO_CONTENT)
    mocked_login = mocker.patch("{{ cookiecutter.project_slug }}.apps.accounts.services.login.LoginService.login", return_value=mocked_response)

    data = {
        "email": "jane@example.com",
        "first_name": "jane",
        "last_name": "doe",
        "password": "super-secret-password",
    }  # nosec
    response = unauthorized_api_client.post(reverse("api-v1-accounts:registration"), data)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert UserAccount.objects.count() == 1
    user = UserAccount.objects.get()
    mocked_login.assert_called_once_with(mocker.ANY, user)
