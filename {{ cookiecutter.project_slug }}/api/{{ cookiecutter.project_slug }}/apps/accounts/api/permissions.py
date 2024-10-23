from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from django.views import View


class IsNotAuthenticated(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:  # noqa: ARG002
        return not request.user.is_authenticated
