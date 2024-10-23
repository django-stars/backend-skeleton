from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from {{ cookiecutter.project_slug }}.apps.accounts.api.v1.serializers.user_profile import UserProfileSerializer
from {{ cookiecutter.project_slug }}.apps.accounts.models import UserAccount


@extend_schema_view(
    get=extend_schema(
        summary="Me",
        tags=["Accounts"],
    ),
    put=extend_schema(
        summary="Update me",
        tags=["Accounts"],
    ),
    patch=extend_schema(
        summary="Update me",
        tags=["Accounts"],
    ),
)
class UserProfileAPIView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> UserAccount:
        return self.request.user
