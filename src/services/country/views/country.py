"""
This module contains the viewsets for the Country model.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, DjangoObjectPermissions

from helpers.auth.custom_jwt import JWTAuth
from helpers.mixins.permissions.policy import (
    PermissionPolicyMixin,
)
from helpers.permissions.model import ModelPermissions
from services.country.filters.country import (
    CountryFilterSet,
)
from services.country.models.country import Country
from services.country.serializers.country import (
    CountrySerializer,
)


class CountryViewSet(
    PermissionPolicyMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    authentication_classes = [JWTAuth]
    permission_classes = [ModelPermissions, DjangoObjectPermissions]

    permission_classes_by_action = {
        "create": [AllowAny],
        "retrieve": [AllowAny],
        "activate": [AllowAny],
    }

    pagination_class = PageNumberPagination
    pagination_class.page_size = 100
    pagination_class.page_size_query_param = "page_size"

    ordering_fields = "__all__"
    ordering = ["-created_at", "-updated_at"]

    filterset_class = CountryFilterSet
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ("domains__name", "name")
