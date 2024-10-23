from typing import ClassVar, cast

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy

from {{ cookiecutter.project_slug }}.apps.common import models as core_models
from {{ cookiecutter.project_slug }}.apps.common.models import CoreModel


class UserManager(core_models.CoreManager, BaseUserManager):
    def create_user(self, email: str, password: str | None = None) -> "UserAccount":
        if not email:
            message = "Users must give an email address"
            raise ValueError(message)

        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str) -> "UserAccount":
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class UserAccount(PermissionsMixin, CoreModel, AbstractBaseUser):
    email = models.EmailField(verbose_name=gettext_lazy("email address"), unique=True)
    first_name = models.CharField(verbose_name=gettext_lazy("first name"), max_length=150, blank=True)
    last_name = models.CharField(verbose_name=gettext_lazy("last name"), max_length=150, blank=True)
    is_staff = models.BooleanField(
        gettext_lazy("staff status"),
        default=False,
        help_text=gettext_lazy("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        gettext_lazy("active"),
        default=True,
        help_text=gettext_lazy(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    class Meta:
        ordering = ("first_name", "last_name")

    def __str__(self) -> str:
        return cast(str, self.email)

    def get_short_name(self) -> str:
        return str(self.email)

    def get_full_name(self) -> str:
        if self.first_name and self.last_name:
            full_name = f"{self.first_name} {self.last_name} <{self.email}>"
        else:
            full_name = self.get_short_name()
        return full_name

    @property
    def notification_salutation(self) -> str:
        if self.first_name and self.last_name:
            salutation = f"{self.first_name} {self.last_name}"
        else:
            salutation = gettext_lazy("Dear client")
        return salutation
