"""
Domain views
Domains are only created using the tenant creation endpoint.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import DjangoObjectPermissions, AllowAny

from helpers.auth.custom_jwt import JWTAuth
from helpers.mixins.permissions.policy import PermissionPolicyMixin
from helpers.permissions.model import ModelPermissions
from services.country.filters.domain import DomainFilterSet
from services.country.models.domain import Domain
from services.country.serializers.domain import DomainSerializer


class DomainViewSet(
    PermissionPolicyMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    API endpoint for Domain model.
    """

    queryset = Domain.objects.all()
    serializer_class = DomainSerializer

    pagination_class = PageNumberPagination
    pagination_class.page_size = 100
    pagination_class.page_size_query_param = "page_size"

    ordering_fields = "__all__"
    ordering = ["-created_at"]

    filterset_class = DomainFilterSet
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = (
        "domain",
        "tenant__name",
    )

    authentication_classes = [JWTAuth]
    permission_classes = [ModelPermissions, DjangoObjectPermissions]

    permission_classes_by_action = {"list": [AllowAny]}
