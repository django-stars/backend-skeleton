from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout

from {{ cookiecutter.project_slug }}.apps.accounts.models import UserAccount


class LoginService:
    @classmethod
    def login(cls, request: Request, user: UserAccount) -> Response:
        cls._django_login(request, user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @classmethod
    def logout(cls, request: Request) -> Response:
        cls._django_logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def _django_logout(request: Request) -> None:  # pragma: no cover
        django_logout(request)

    @staticmethod
    def _django_login(request: Request, user: UserAccount) -> None:  # pragma: no cover
        django_login(request, user)
