from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from {{ cookiecutter.project_slug }}.apps.accounts.exceptions import (
    InvalidPasswordError,
    InvalidResetPasswordSignatureError,
    WrongPasswordError,
)
from {{ cookiecutter.project_slug }}.apps.accounts.services.password import PasswordService


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(max_length=128, write_only=True, style={"input_type": "password"})
    new_password = serializers.CharField(max_length=128, write_only=True, style={"input_type": "password"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get("request")
        self.user = getattr(self.request, "user", None)
        self.password_service = PasswordService()

    def validate_old_password(self, old_password):
        try:
            self.password_service.check_password(self.user, old_password)
        except WrongPasswordError as e:
            raise serializers.ValidationError(e.message) from e
        return old_password

    def validate_new_password(self, new_password):
        try:
            self.password_service.validate_password(new_password, user=self.user)
        except InvalidPasswordError as e:
            raise serializers.ValidationError(e.messages) from e
        return new_password

    def create(self, validated_data):
        assert False, "Do not use update directly"

    def update(self, instance, validated_data):
        assert False, "Do not use update directly"

    def save(self, **kwargs):
        self.password_service.change_password(self.user, self.validated_data["new_password"])


class ConfirmResetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=128, write_only=True, style={"input_type": "password"})
    signature = serializers.CharField(max_length=71, write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password_service = PasswordService()

    def validate_password(self, password):
        try:
            self.password_service.validate_password(password)
        except InvalidPasswordError as e:
            raise ValidationError(e) from e
        return password

    def save(self, **kwargs):
        new_password = self.validated_data["password"]
        signature = self.validated_data["signature"]
        try:
            self.password_service.reset_password(signature, new_password)
        except InvalidResetPasswordSignatureError as e:
            raise ValidationError({"signature": e.message}) from e

    def create(self, validated_data):
        assert False, "Do not use update directly"

    def update(self, instance, validated_data):
        assert False, "Do not use update directly"


class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=128, write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password_service = PasswordService()

    def save(self, **kwargs):
        email = self.validated_data["email"]
        self.password_service.send_reset_password_link(email)

    def create(self, validated_data):
        assert False, "Do not use update directly"

    def update(self, instance, validated_data):
        assert False, "Do not use update directly"
