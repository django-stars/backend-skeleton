from rest_framework.authentication import SessionAuthentication


class CustomSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        """
        Exempt CSRF for session based authentication "application/json".
        """
        if request.content_type != "application/json":
            super().enforce_csrf(request)
