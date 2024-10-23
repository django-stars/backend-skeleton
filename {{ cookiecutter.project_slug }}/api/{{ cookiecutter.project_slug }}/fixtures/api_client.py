import json

from collections.abc import Callable
from typing import Any

import pytest

from rest_framework.response import Response
from rest_framework.test import APIClient

from {{ cookiecutter.project_slug }}.apps.accounts.models import UserAccount
from {{ cookiecutter.project_slug }}.fixtures.user_account import UserAccountMaker


class _CustomAPIClient(APIClient):
    """
    Helper APIClient class

    As we use `rest_framework.parsers.JSONParser` only we need to make correct
    requests during test run:
        `content_type` should explicitly set to "application/json"
        `data should` properly encoded to JSON.
    """

    def post(
        self,
        path: str,
        data: Any = None,  # noqa: ANN401
        format: str | None = None,  # noqa: A002
        content_type: str = "application/json",
        *,
        follow: bool = False,
        **extra,  # noqa: ANN003
    ) -> Response:
        if isinstance(data, dict | list):
            data = json.dumps(data)
        response = super().post(path, data=data, format=format, content_type=content_type, follow=follow, **extra)
        return response

    def put(
        self,
        path: str,
        data: Any = None,  # noqa: ANN401
        format: str | None = None,  # noqa: A002
        content_type: str = "application/json",
        *,
        follow: bool = False,
        **extra,  # noqa: ANN003
    ) -> Response:
        if isinstance(data, dict | list):
            data = json.dumps(data)
        response = super().put(path, data=data, format=format, content_type=content_type, follow=follow, **extra)
        return response

    def patch(
        self,
        path: str,
        data: Any = None,  # noqa: ANN401
        format: str | None = None,  # noqa: A002
        content_type: str = "application/json",
        *,
        follow: bool = False,
        **extra,  # noqa: ANN003
    ) -> Response:
        if isinstance(data, dict | list):
            data = json.dumps(data)
        response = super().patch(path, data=data, format=format, content_type=content_type, follow=follow, **extra)
        return response

    def delete(
        self,
        path: str,
        data: Any = None,  # noqa: ANN401
        format: str | None = None,  # noqa: A002
        content_type: str = "application/json",
        *,
        follow: bool = False,
        **extra,  # noqa: ANN003
    ) -> Response:
        if isinstance(data, dict | list):
            data = json.dumps(data)
        response = super().delete(path, data=data, format=format, content_type=content_type, follow=follow, **extra)
        return response


type CustomAPIClient = _CustomAPIClient
type ApiClientMaker = Callable[..., CustomAPIClient]


@pytest.fixture
def unauthorized_api_client() -> CustomAPIClient:
    return _CustomAPIClient()


@pytest.fixture
def api_client(user_account: UserAccountMaker) -> ApiClientMaker:
    def _api_client(auth_user: UserAccount | None) -> CustomAPIClient:
        if auth_user is None:
            auth_user = user_account()
        client = _CustomAPIClient()
        client.force_authenticate(auth_user)
        return client

    return _api_client
