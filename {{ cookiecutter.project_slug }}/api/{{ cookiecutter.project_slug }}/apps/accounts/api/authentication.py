from rest_framework.authentication import SessionAuthentication
from rest_framework.request import Request


class CustomSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request: Request) -> None:
        """
        Exempt CSRF for session based authentication "application/json".
        """
        if request.content_type != "application/json":
            super().enforce_csrf(request)
