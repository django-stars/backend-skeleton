from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.utils.translation import gettext

from {{ cookiecutter.project_slug }}.apps.accounts.exceptions import InvalidPasswordError
from {{ cookiecutter.project_slug }}.apps.accounts.models import UserAccount
from {{ cookiecutter.project_slug }}.apps.accounts.services.password import PasswordService


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, max_length=128)
    password = serializers.CharField(write_only=True, max_length=128)
    first_name = serializers.CharField(required=True, max_length=30)
    last_name = serializers.CharField(required=True, max_length=30)

    class Meta:
        model = UserAccount
        fields = ("email", "first_name", "last_name", "password")

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002 ANN003
        super().__init__(*args, **kwargs)
        self.password_service = PasswordService()

    def validate_email(self, email: str) -> str:
        if UserAccount.objects.filter(email=email).exists():
            raise ValidationError(gettext("Could not create account with this email."))
        return super().validate(email)

    def validate_password(self, new_password: str) -> str:
        try:
            self.password_service.validate_password(new_password)
        except InvalidPasswordError as e:
            raise serializers.ValidationError(e.messages) from e
        return new_password

    def save(self, **kwargs) -> UserAccount:  # noqa: ANN003
        self.instance = super().save(**kwargs)
        raw_password = self.validated_data.get("password")
        self.instance.set_password(raw_password)
        self.instance.save()
        return self.instance
