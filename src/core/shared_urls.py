"""
G project urls.
"""
import debug_toolbar
from django.conf import settings
from django.contrib.staticfiles import views
from django.urls import path, include, re_path

from core.docs import urlpatterns as docs_urls  # noqa # pylint: disable=import-error

urlpatterns = [
    *docs_urls,
    path("", include("django_prometheus.urls")),
    path("countries/", include("services.country.urls.country")),
    path("countries/", include("services.country.urls.domain")),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r"^static/(?P<path>.*)$", views.serve),
    ]
