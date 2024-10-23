from collections.abc import Callable

import pytest

from model_bakery import baker

from {{ cookiecutter.project_slug }}.apps.accounts.models import UserAccount


type UserAccountMaker = Callable[..., UserAccount]


@pytest.fixture
def user_account(db: None) -> UserAccountMaker:  # noqa: ARG001
    def _user(**kwargs) -> UserAccount:  # noqa: ANN003
        return baker.make("accounts.UserAccount", **kwargs)

    return _user
