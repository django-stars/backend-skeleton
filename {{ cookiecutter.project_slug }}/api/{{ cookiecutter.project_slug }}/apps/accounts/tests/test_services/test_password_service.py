import uuid

import pytest

from pytest_mock import MockerFixture

from django.conf import LazySettings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner

from {{ cookiecutter.project_slug }}.apps.accounts.exceptions import (
    InvalidPasswordError,
    InvalidResetPasswordSignatureError,
    WrongPasswordError,
)
from {{ cookiecutter.project_slug }}.apps.accounts.models import UserAccount
from {{ cookiecutter.project_slug }}.apps.accounts.services.password import PasswordService
from {{ cookiecutter.project_slug }}.fixtures.user_account import UserAccountMaker


PASSWORD_SERVICE_PATH = "{{ cookiecutter.project_slug }}.apps.accounts.services.password.PasswordService"  # nosec


def test_change_password(user_account: UserAccountMaker) -> None:
    old_password = "old_password_1234"  # nosec
    new_password = "new_password_5678"  # nosec

    user = user_account()
    user.set_password(old_password)
    user.save(update_fields=("password",))
    assert user.check_password(old_password)

    PasswordService.change_password(user, new_password)

    user.refresh_from_db()
    assert user.check_password(new_password)


def test_check_password(user_account: UserAccountMaker) -> None:
    user = user_account()
    user.set_password("CORRECT_PASSWORD")
    user.save(update_fields=("password",))

    with pytest.raises(WrongPasswordError):
        PasswordService.check_password(user, "INCORRECT_PASSWORD")


def test_validate_password(mocker: MockerFixture) -> None:
    mocker.patch("django.contrib.auth.password_validation.validate_password", side_effect=ValidationError("exception"))

    with pytest.raises(InvalidPasswordError):
        PasswordService.validate_password("SOME_PASSWORD")


def test_generate_reset_password_signature(user_account: UserAccountMaker) -> None:
    user = user_account()
    expected_reset_password_signature = TimestampSigner().sign(user.pk)
    generated_reset_password_signature = PasswordService._generate_reset_password_signature(user)  # noqa: SLF001

    assert generated_reset_password_signature == expected_reset_password_signature


def test_reset_password_success(user_account: UserAccountMaker, mocker: MockerFixture) -> None:
    new_password = "new_password_1234"  # nosec
    user = user_account()
    reset_password_signature = TimestampSigner().sign(user.pk)
    mocked_change_password = mocker.patch(f"{PASSWORD_SERVICE_PATH}.change_password")

    PasswordService.reset_password(reset_password_signature, new_password)

    mocked_change_password.assert_called_once_with(user, new_password)


@pytest.mark.django_db
@pytest.mark.parametrize("exception", [SignatureExpired, BadSignature])
def test_reset_password_signature_failure(
    mocker: MockerFixture, settings: LazySettings, exception: type[Exception]
) -> None:
    new_password = "new_password_1234"  # nosec
    reset_password_signature = "reset_password_signature"  # nosec
    mocker.patch("django.core.signing.TimestampSigner.unsign", side_effect=exception("Some message"))
    settings.{{ cookiecutter.project_slug }}_RESET_PASSWORD_EXPIRATION_DELTA = 42
    mocked_change_password = mocker.patch(f"{PASSWORD_SERVICE_PATH}.change_password")

    with pytest.raises(InvalidResetPasswordSignatureError):
        PasswordService.reset_password(reset_password_signature, new_password)

    assert mocked_change_password.call_count == 0


@pytest.mark.django_db
def test_reset_password_user_failure(mocker: MockerFixture) -> None:
    new_password = "new_password_1234"  # nosec
    assert UserAccount.objects.count() == 0
    reset_password_signature = TimestampSigner().sign(uuid.uuid4())
    mocked_change_password = mocker.patch(f"{PASSWORD_SERVICE_PATH}.change_password")

    with pytest.raises(InvalidResetPasswordSignatureError):
        PasswordService.reset_password(reset_password_signature, new_password)

    assert mocked_change_password.call_count == 0


@pytest.mark.django_db
def test_send_reset_password_link_success(
    settings: LazySettings, user_account: UserAccountMaker, mocker: MockerFixture
) -> None:
    user = user_account()
    domain_name = "test_send_reset_password_link_success.com"
    signature = "signature"
    site = Site.objects.create(domain=domain_name, name=domain_name)
    settings.SITE_ID = site.pk
    mocked_generate_reset_password_signature = mocker.patch(
        f"{PASSWORD_SERVICE_PATH}._generate_reset_password_signature", return_value=signature
    )
    mocked_send_notification = mocker.patch(f"{PASSWORD_SERVICE_PATH}._send_notification")

    PasswordService.send_reset_password_link(user.email)

    mocked_generate_reset_password_signature.assert_called_once_with(user)
    mocked_send_notification.assert_called_once_with(
        user.pk,
        {
            "user_notification_salutation": "Dear client",
            "domain_name": domain_name,
            "reset_password_link": f"https://{domain_name}/reset-password/{signature}",
        },
    )


@pytest.mark.django_db
def test_send_reset_password_link_failure(mocker: MockerFixture) -> None:
    assert UserAccount.objects.count() == 0
    mocked_generate_reset_password_signature = mocker.patch(
        f"{PASSWORD_SERVICE_PATH}._generate_reset_password_signature"
    )
    mocked_send_notification = mocker.patch(f"{PASSWORD_SERVICE_PATH}._send_notification")

    PasswordService.send_reset_password_link("non-exisiting-user@example.com")

    assert mocked_generate_reset_password_signature.call_count == 0
    assert mocked_send_notification.call_count == 0
