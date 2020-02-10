from django.core.exceptions import ValidationError


class AccountError(ValidationError):

    pass


class InvalidPasswordError(AccountError):

    pass


class WrongPasswordError(AccountError):

    pass


class InvalidResetPasswordSignatureError(AccountError):

    pass
