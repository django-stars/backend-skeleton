from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.utils.translation import gettext

from {{ cookiecutter.project_slug }}.apps.accounts.exceptions import (
    InvalidPasswordError,
    InvalidResetPasswordSignatureError,
    WrongPasswordError,
)
from {{ cookiecutter.project_slug }}.apps.accounts.models import UserAccount


class PasswordService:
    @staticmethod
    def change_password(user: UserAccount, new_password: str) -> None:
        user.set_password(new_password)
        user.save(update_fields=("password",))

    @staticmethod
    def check_password(user: UserAccount, password: str) -> None:
        if not user.check_password(password):
            raise WrongPasswordError(gettext("Incorrect password."))

    @staticmethod
    def validate_password(password: str, user: UserAccount = None) -> None:
        try:
            password_validation.validate_password(password, user=user)
        except DjangoValidationError as e:
            raise InvalidPasswordError(e.messages) from e

    @classmethod
    def send_reset_password_link(cls, email: str) -> None:
        try:
            user = UserAccount.objects.active().get(email=email)
        except UserAccount.DoesNotExist:
            pass
        else:
            reset_password_signature = cls._generate_reset_password_signature(user)
            domain_name = Site.objects.get_current().domain
            reset_password_link = f"https://{domain_name}/reset-password/{reset_password_signature}"
            context = {
                "user_notification_salutation": user.notification_salutation,
                "domain_name": domain_name,
                "reset_password_link": reset_password_link,
            }
            cls._send_notification(user.pk, context)

    @classmethod
    def reset_password(cls, signature: str, new_password: str) -> None:
        signer = TimestampSigner()
        try:
            user_pk = signer.unsign(signature, max_age=settings.{{ cookiecutter.__env_prefix }}RESET_PASSWORD_EXPIRATION_DELTA)
            user = UserAccount.objects.active().get(pk=user_pk)
        except (SignatureExpired, BadSignature, UserAccount.DoesNotExist) as e:
            raise InvalidResetPasswordSignatureError(gettext("Invalid confirmation code or user does not exist")) from e

        cls.change_password(user, new_password)

    @staticmethod
    def _send_notification(user_pk: str, context: dict) -> None:
        # TODO @bulya: Implement notification sending  # noqa: FIX002
        # DI-2715
        # send_notification.delay(user_pk, "user-reset-password", context)  # noqa: ERA001
        pass

    @staticmethod
    def _generate_reset_password_signature(user: UserAccount) -> str:
        signer = TimestampSigner()
        return signer.sign(user.pk)
