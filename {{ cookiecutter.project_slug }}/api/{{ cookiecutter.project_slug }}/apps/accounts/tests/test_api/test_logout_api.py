from django.urls import reverse

from rest_framework import status
from rest_framework.response import Response

import pytest


@pytest.mark.django_db
def test_logout_api_success(user_account, api_client, mocker):
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
