
"""
    Yoona.ai project urls.
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles import views
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # django
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),

    # jwt
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # custom
    path("users/", include("services.user.urls.user")),
    path("countries/", include("services.country.urls.country")),
    path("countries/", include("services.country.urls.domain")),

    # prometheus
    path("", include("django_prometheus.urls")),
]

# static files (images, css, javascript, etc.) for development only.
if settings.DEBUG:
    urlpatterns += [
        re_path(r"^static/(?P<path>.*)$", views.serve),
    ]
