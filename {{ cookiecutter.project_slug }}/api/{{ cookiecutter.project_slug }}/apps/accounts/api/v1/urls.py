from django.urls import path

from {{ cookiecutter.project_slug }}.apps.accounts.api.v1.views.login import LoginView, LogoutView
from {{ cookiecutter.project_slug }}.apps.accounts.api.v1.views.password import (
    ChangePasswordAPIView,
    ConfirmResetPasswordAPIView,
    ResetPasswordAPIView,
)
from {{ cookiecutter.project_slug }}.apps.accounts.api.v1.views.registration import RegistrationAPIView
from {{ cookiecutter.project_slug }}.apps.accounts.api.v1.views.user_profile import UserProfileAPIView


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", UserProfileAPIView.as_view(), name="user-profile"),
    path("password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("password/confirm/", ConfirmResetPasswordAPIView.as_view(), name="confirm-reset-password"),
    path("password/reset/", ResetPasswordAPIView.as_view(), name="reset-password"),
    path("registration/", RegistrationAPIView.as_view(), name="registration"),
]
