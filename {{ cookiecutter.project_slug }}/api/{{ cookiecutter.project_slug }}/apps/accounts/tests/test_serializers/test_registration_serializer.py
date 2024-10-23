import pytest

from pytest_mock import MockerFixture
from rest_framework.exceptions import ValidationError

from {{ cookiecutter.project_slug }}.apps.accounts.api.v1.serializers.registration import RegistrationSerializer
from {{ cookiecutter.project_slug }}.apps.accounts.exceptions import InvalidPasswordError
from {{ cookiecutter.project_slug }}.apps.accounts.models import UserAccount
from {{ cookiecutter.project_slug }}.fixtures.user_account import UserAccountMaker


@pytest.fixture
def input_data() -> dict[str, str]:
    return {
        "email": "jane@example.com",
        "password": "test12356",  # nosec
        "first_name": "first_name",
        "last_name": "last_name",
    }


def test_registration_serializer_validate_success(input_data: dict) -> None:
    serializer = RegistrationSerializer(data=input_data)
    data = serializer.validate(input_data)
    assert data == input_data


def test_registration_serializer_validate_password_success(mocker: MockerFixture, input_data: dict) -> None:
    serializer = RegistrationSerializer(data=input_data)
    mocked_validate_password = mocker.patch.object(serializer.password_service, "validate_password")

    validated_password = serializer.validate_password(input_data["password"])

    assert validated_password == input_data["password"]
    mocked_validate_password.assert_called_once_with(input_data["password"])


def test_registration_serializer_validate_password_failure(mocker: MockerFixture, input_data: dict) -> None:
    serializer = RegistrationSerializer(data=input_data)
    mocked_validate_password = mocker.patch.object(
        serializer.password_service, "validate_password", side_effect=[InvalidPasswordError("error")]
    )

    with pytest.raises(ValidationError):
        serializer.validate_password(input_data["password"])

    mocked_validate_password.assert_called_once_with(input_data["password"])


@pytest.mark.django_db
def test_registration_serializer_validate_email_success(user_account: UserAccountMaker, input_data: dict) -> None:
    user_account(email="john@example.com")
    serializer = RegistrationSerializer(data=input_data)
    validated_email = serializer.validate_email(input_data["email"])
    assert validated_email == input_data["email"]


@pytest.mark.django_db
def test_registration_serializer_validate_email_failure(user_account: UserAccountMaker, input_data: dict) -> None:
    user_account(email=input_data["email"])
    serializer = RegistrationSerializer(data=input_data)
    with pytest.raises(ValidationError):
        serializer.validate_email(input_data["email"])


@pytest.mark.django_db
def test_registration_serializer_save_success(input_data: dict) -> None:
    assert UserAccount.objects.count() == 0

    serializer = RegistrationSerializer(data=input_data)
    serializer.is_valid()
    user = serializer.save()

    assert UserAccount.objects.count() == 1
    assert UserAccount.objects.get().pk == user.pk
    assert user.email == input_data["email"]
    assert user.first_name == input_data["first_name"]
    assert user.last_name == input_data["last_name"]
    assert user.has_usable_password()
    assert user.check_password(input_data["password"])
