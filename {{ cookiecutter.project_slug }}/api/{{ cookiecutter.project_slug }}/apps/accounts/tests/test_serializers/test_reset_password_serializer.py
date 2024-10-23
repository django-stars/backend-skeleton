from pytest_mock import MockerFixture

from {{ cookiecutter.project_slug }}.apps.accounts.api.v1.serializers.password import ResetPasswordSerializer


def test_save(mocker: MockerFixture) -> None:
    email = "jane@example.com"
    serializer = ResetPasswordSerializer(data={"email": email})
    mocked_send_reset_password_link = mocker.patch.object(serializer.password_service, "send_reset_password_link")

    serializer.is_valid()
    serializer.save()

    mocked_send_reset_password_link.assert_called_once_with(email)
