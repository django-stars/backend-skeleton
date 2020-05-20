from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path


PLATFORM_PREFIX = "_platform"
API_PREFIX = "api"
DOCS_PREFIX = "docs"

admin_urlpatterns = [
    path("admin/", admin.site.urls),
]

api_v1_urlpatterns = [
    path(
        f"{API_PREFIX}/v1/accounts/",
        include(("{{ cookiecutter.project_slug }}.apps.accounts.api.v1.urls", "accounts"), namespace="api-v1-accounts"),
    )
]

urlpatterns = admin_urlpatterns + api_v1_urlpatterns

# enable Swagger
if "SWAGGER" in settings.{{ cookiecutter.project_slug | upper() }}_FEATURES:
    from rest_framework import permissions

    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view

    api_v1_schema_view = get_schema_view(
        openapi.Info(
            title="{{ cookiecutter.project_name }}",
            default_version="v1",
            description="{{ cookiecutter.project_name }} API v1 description",
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
        patterns=api_v1_urlpatterns,
    )

    swagger_urlpatterns = [
        re_path(
            f"{PLATFORM_PREFIX}/{DOCS_PREFIX}/v1/" + r"swagger(?P<format>\.json|\.yaml)$",
            api_v1_schema_view.without_ui(cache_timeout=0),
            name="v1-schema-json",
        ),
        path(
            f"{PLATFORM_PREFIX}/{DOCS_PREFIX}/v1/swagger/",
            api_v1_schema_view.with_ui("swagger", cache_timeout=0),
            name="v1-schema-swagger-ui",
        ),
        path(
            f"{PLATFORM_PREFIX}/{DOCS_PREFIX}/v1/redoc/",
            api_v1_schema_view.with_ui("redoc", cache_timeout=0),
            name="v1-schema-redoc",
        ),
    ]

    urlpatterns += swagger_urlpatterns

# enable serve static by django for local develop
if settings.DEBUG:  # pragma: no cover
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# enable debug_toolbar for local develop (if installed)
if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]


# enable Sentry check (by raising 500 on demand)
if not settings.DEBUG:
    from django.views.generic.base import View

    class ServerErrorTestView(View):
        def dispatch(self, request, *args, **kwargs):
            assert False, "Server error test: response with 500 HTTP status code"

    urlpatterns += [path(f"{PLATFORM_PREFIX}/500-error-test/", ServerErrorTestView.as_view())]
