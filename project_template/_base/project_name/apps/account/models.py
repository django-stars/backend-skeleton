from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from {{ project_name }}.apps.common.models import CoreModel
from . import managers


class User(PermissionsMixin, CoreModel, AbstractBaseUser):
    email = models.EmailField(verbose_name=_('Email'), unique=True)
    first_name = models.CharField(
        verbose_name=_('first name'),
        max_length=30,
        blank=True, null=True
    )
    last_name = models.CharField(
        verbose_name=_('last name'),
        max_length=30,
        blank=True, null=True
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField(default=timezone.now)

    objects = managers.UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('first_name', 'last_name', )

    def __str__(self):
        return self.get_full_name() or self.email

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        return self.email.split('@')[0]

    def get_full_name(self):
        return ' '.join(filter(None, [self.first_name, self.last_name]))
