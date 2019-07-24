from django.contrib.auth import forms

from . import models


class AdminUserChangeForm(forms.UserChangeForm):
    class Meta:
        model = models.User
        fields = "__all__"
