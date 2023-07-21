
"""
    Documentation for the Yoona.ai API.
"""
from django.urls import re_path, path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from config.settings import env

# from config import settings  # noqa # pylint: disable=import-error

SchemaView = get_schema_view(
    openapi.Info(
        title="Guide API",
        default_version="v1",
        description="Guide API v1 documentation",
        contact=openapi.Contact(email="kamranvalijonov@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    url=env.str_env("API_BASE_URL", "http://localhost"),
    permission_classes=[
        permissions.AllowAny,
    ],
    patterns=[
        path("", include("core.urls")),
        path("", include("core.shared_urls")),
    ],
)

# pylint: disable=no-member
urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        SchemaView.without_ui(cache_timeout=0),  # noqa
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        SchemaView.with_ui("swagger", cache_timeout=0),  # noqa
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$",
        SchemaView.with_ui("redoc", cache_timeout=0),  # noqa
        name="schema-redoc",
    ),
]
