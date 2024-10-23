import pytest

from pytest_mock import MockerFixture
from rest_framework.exceptions import ValidationError

from {{ cookiecutter.project_slug }}.apps.accounts.api.v1.serializers.password import ConfirmResetPasswordSerializer
from {{ cookiecutter.project_slug }}.apps.accounts.exceptions import InvalidPasswordError, InvalidResetPasswordSignatureError


NEW_PASSWORD = "NEW_PASSWORD"  # nosec
RESET_PASSWORD_SIGNATURE = "SIGNATURE"  # nosec


def test_validate_password_success(mocker: MockerFixture) -> None:
    serializer = ConfirmResetPasswordSerializer()
    mocked_validate_password = mocker.patch.object(serializer.password_service, "validate_password")

    result = serializer.validate_password(NEW_PASSWORD)

    assert result == NEW_PASSWORD
    mocked_validate_password.assert_called_once_with(NEW_PASSWORD)


def test_validate_password_failure(mocker: MockerFixture) -> None:
    serializer = ConfirmResetPasswordSerializer()
    mocked_validate_password = mocker.patch.object(
        serializer.password_service, "validate_password", side_effect=InvalidPasswordError("message")
    )

    with pytest.raises(ValidationError):
        serializer.validate_password(NEW_PASSWORD)

    mocked_validate_password.assert_called_once_with(NEW_PASSWORD)


def test_save_success(mocker: MockerFixture) -> None:
    serializer = ConfirmResetPasswordSerializer(data={"password": NEW_PASSWORD, "signature": RESET_PASSWORD_SIGNATURE})
    mocker.patch.object(serializer, "validate_password", return_value=NEW_PASSWORD)
    mocked_reset_password = mocker.patch.object(serializer.password_service, "reset_password")

    serializer.is_valid()
    serializer.save()

    mocked_reset_password.assert_called_once_with(RESET_PASSWORD_SIGNATURE, NEW_PASSWORD)


def test_save_failure(mocker: MockerFixture) -> None:
    serializer = ConfirmResetPasswordSerializer(data={"password": NEW_PASSWORD, "signature": RESET_PASSWORD_SIGNATURE})
    mocker.patch.object(serializer, "validate_password", return_value=NEW_PASSWORD)
    mocked_reset_password = mocker.patch.object(
        serializer.password_service, "reset_password", side_effect=InvalidResetPasswordSignatureError("message")
    )

    serializer.is_valid()
    with pytest.raises(ValidationError):
        serializer.save()

    mocked_reset_password.assert_called_once_with(RESET_PASSWORD_SIGNATURE, NEW_PASSWORD)
