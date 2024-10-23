import pytest

from rest_framework.exceptions import ValidationError

from {{ cookiecutter.project_slug }}.apps.accounts.api.v1.serializers.login import LoginSerializer
from {{ cookiecutter.project_slug }}.fixtures.user_account import UserAccountMaker


@pytest.mark.django_db
def test_login_serializer_validate_success(user_account: UserAccountMaker) -> None:
    email = "jane@example.com"
    password = "super_secret_password"  # nosec
    user = user_account(email=email)
    user.set_password(password)
    user.save(update_fields=("password",))
    serializer = LoginSerializer()

    result = serializer.validate({"email": email, "password": password})
    assert result == {"user": user}


@pytest.mark.django_db
def test_login_serializer_validate_failure(user_account: UserAccountMaker) -> None:
    email = "jane@example.com"
    password = "super_secret_password"  # nosec
    user = user_account(email=email)
    user.set_password(password)
    user.save(update_fields=("password",))
    serializer = LoginSerializer()

    with pytest.raises(ValidationError):
        serializer.validate({"email": email, "password": "incorrect"})
