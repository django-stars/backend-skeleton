import pytest

from pytest_mock import MockerFixture
from rest_framework import status
from rest_framework.response import Response

from django.urls import reverse

from {{ cookiecutter.project_slug }}.fixtures.api_client import ApiClientMaker
from {{ cookiecutter.project_slug }}.fixtures.user_account import UserAccountMaker


@pytest.mark.django_db
def test_logout_api_success(user_account: UserAccountMaker, api_client: ApiClientMaker, mocker: MockerFixture) -> None:
    user = user_account()
    client = api_client(auth_user=user)
    mocked_logout = mocker.patch(
        "{{ cookiecutter.project_slug }}.apps.accounts.services.login.LoginService.logout",
        return_value=Response(status=status.HTTP_204_NO_CONTENT),
    )

    response = client.post(reverse("api-v1-accounts:logout"))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data is None
    assert mocked_logout.call_count == 1
