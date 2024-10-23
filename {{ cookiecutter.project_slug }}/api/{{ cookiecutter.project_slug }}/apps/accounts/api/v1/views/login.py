from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from {{ cookiecutter.project_slug }}.apps.accounts.api.permissions import IsNotAuthenticated
from {{ cookiecutter.project_slug }}.apps.accounts.api.v1.serializers.login import LoginSerializer
from {{ cookiecutter.project_slug }}.apps.accounts.services.login import LoginService


class LoginView(GenericAPIView):
    permission_classes = (IsNotAuthenticated,)
    serializer_class = LoginSerializer

    @extend_schema(summary="Login", tags=["Accounts"], responses={status.HTTP_204_NO_CONTENT: OpenApiResponse()})
    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        response = LoginService.login(request, user)
        return response


class LogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(summary="Log out", tags=["Accounts"], responses={status.HTTP_204_NO_CONTENT: OpenApiResponse()})
    def post(self, request: Request) -> Response:
        response = LoginService.logout(request)
        return response
