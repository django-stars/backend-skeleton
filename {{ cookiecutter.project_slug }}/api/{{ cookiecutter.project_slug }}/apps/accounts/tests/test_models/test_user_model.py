import pytest

from {{ cookiecutter.project_slug }}.apps.accounts.models import UserAccount
from {{ cookiecutter.project_slug }}.fixtures.user_account import UserAccountMaker


@pytest.mark.django_db
def test_core_queryset_active(user_account: UserAccountMaker) -> None:
    assert not UserAccount.objects.exists()

    total_users_count = 3
    active_user = user_account(is_active=True)
    user_account(is_active=False)
    user_account(is_active=False)

    assert UserAccount.objects.count() == total_users_count
    assert UserAccount.objects.active().get() == active_user


@pytest.mark.django_db
def test_core_queryset_inactive(user_account: UserAccountMaker) -> None:
    assert not UserAccount.objects.exists()

    inactive_user = user_account(is_active=False)
    user_account(is_active=True)
    user_account(is_active=True)
    expected_total_users_count = 3
    expected_inactive_users_count = 1

    assert UserAccount.objects.count() == expected_total_users_count
    assert UserAccount.objects.inactive().count() == expected_inactive_users_count
    assert UserAccount.objects.inactive().first() == inactive_user


@pytest.mark.django_db
def test_core_queryset_activate(user_account: UserAccountMaker) -> None:
    assert not UserAccount.objects.exists()

    user = user_account(is_active=False)

    assert not UserAccount.objects.active().exists()
    assert UserAccount.objects.inactive().get() == user

    user.activate()

    assert not UserAccount.objects.inactive().exists()
    assert UserAccount.objects.active().get() == user


@pytest.mark.django_db
def test_core_queryset_deactivate(user_account: UserAccountMaker) -> None:
    assert not UserAccount.objects.exists()

    user = user_account(is_active=True)

    assert not UserAccount.objects.inactive().exists()
    assert UserAccount.objects.active().get() == user

    user.deactivate()

    assert UserAccount.objects.count() == 1
    assert not UserAccount.objects.active().exists()
    assert UserAccount.objects.inactive().get() == user


@pytest.mark.django_db
def test_create_user_success() -> None:
    assert not UserAccount.objects.exists()

    user_email = "jane@example.com"
    user_password = "super-secret-password"  # nosec
    user = UserAccount.objects.create_user(user_email, user_password)

    assert UserAccount.objects.get() == user
    assert user.email == user_email
    assert not user.is_staff
    assert not user.is_superuser
    assert user.check_password(user_password)


@pytest.mark.django_db
def test_create_user_no_email_failure() -> None:
    assert not UserAccount.objects.exists()

    with pytest.raises(ValueError, match="Users must give an email address"):
        UserAccount.objects.create_user(None)

    assert not UserAccount.objects.exists()


@pytest.mark.django_db
def test_create_superuser_success() -> None:
    assert not UserAccount.objects.exists()

    superuser_email = "admin@example.com"
    superuser_password = "super-secret-password"  # nosec
    superuser = UserAccount.objects.create_superuser(superuser_email, superuser_password)

    assert UserAccount.objects.get() == superuser
    assert superuser.email == superuser_email
    assert superuser.is_staff
    assert superuser.is_superuser
    assert superuser.check_password(superuser_password)


@pytest.mark.django_db
def test_create_superuser_no_email_failure() -> None:
    assert not UserAccount.objects.exists()

    with pytest.raises(ValueError, match="Users must give an email address"):
        UserAccount.objects.create_superuser(None, None)

    assert not UserAccount.objects.exists()


@pytest.mark.parametrize("email", ["jane@example.com", "john@example.com"])
@pytest.mark.django_db
def test_get_short_name(user_account: UserAccountMaker, email: str) -> None:
    assert not UserAccount.objects.exists()

    user = user_account(email=email)

    assert UserAccount.objects.get() == user
    assert user.get_short_name() == user.email


@pytest.mark.parametrize(
    ("first_name", "last_name", "email", "expected"),
    [
        ("Jane", "Doe", "jane@example.com", "Jane Doe <jane@example.com>"),
        ("", "", "jane@example.com", "jane@example.com"),
        ("", "Doe", "jane@example.com", "jane@example.com"),
        ("Jane", "", "jane@example.com", "jane@example.com"),
    ],
)
@pytest.mark.django_db
def test_get_full_name(
    user_account: UserAccountMaker, first_name: str, last_name: str, email: str, expected: str
) -> None:
    assert not UserAccount.objects.exists()

    user = user_account(first_name=first_name, last_name=last_name, email=email)

    assert UserAccount.objects.get() == user
    assert user.get_full_name() == expected


@pytest.mark.parametrize(
    ("first_name", "last_name", "expected"), [("Jane", "Doe", "Jane Doe"), ("", "", "Dear client")]
)
@pytest.mark.django_db
def test_notification_salutation(
    user_account: UserAccountMaker, first_name: str, last_name: str, expected: str
) -> None:
    user = user_account(first_name=first_name, last_name=last_name)
    assert user.notification_salutation == expected
