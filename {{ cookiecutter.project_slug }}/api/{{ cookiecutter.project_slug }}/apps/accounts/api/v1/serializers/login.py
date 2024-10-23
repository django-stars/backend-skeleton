from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.auth import authenticate as django_authenticate
from django.utils.translation import gettext

from {{ cookiecutter.project_slug }}.apps.accounts.models import UserAccount


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, max_length=254)
    password = serializers.CharField(max_length=128, style={"input_type": "password"}, write_only=True)

    @staticmethod
    def _authenticate(email: str, password: str) -> UserAccount | None:
        return django_authenticate(email=email, password=password)  # pragma: no cover

    def validate(self, attrs: dict) -> dict:
        user = self._authenticate(attrs.get("email"), attrs.get("password"))
        if user:
            return {"user": user}
        raise ValidationError(gettext("Incorrect email or password."))

    def create(self, validated_data: dict) -> None:  # noqa: ARG002
        message = "Do not use create directly"
        raise AssertionError(message)

    def update(self, instance: dict, validated_data: dict) -> None:  # noqa: ARG002
        message = "Do not use update directly"
        raise AssertionError(message)
