from abc import ABC
from collections import defaultdict

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from helpers.validators.domain import DomainFormatValidator
from services.country.models.domain import Domain
from helpers.validators.list_unique import ListUniqueValidator


class UniquenessListSerializer(serializers.ListSerializer, ABC):
    """
    List serializer that checks for uniqueness of the given field
    """

    validators = [ListUniqueValidator(unique_field_names=["domain"])]

    def is_valid(self, *, raise_exception=False):
        """
        Check if the serializer is valid
        The following rules are checked:
        1. The domain objects domain is unique
        2. Only single primary domain object is allowed for the company
        """

        # pylint: disable=protected-access
        # check if the company already had a primary domain
        # and if the new domain is also primary raise an error
        tenant_db_table = self.child.Meta.model._meta.get_field(  # noqa
            "tenant"
        ).related_model._meta.db_table
        model_db_table = self.child.Meta.model._meta.db_table
        sql = f"""
            SELECT {model_db_table}.*, {tenant_db_table}.name
            FROM {model_db_table}
            JOIN {tenant_db_table}
                ON {model_db_table}.tenant_id = {tenant_db_table}.id
            WHERE {tenant_db_table}.name in %s
        """
        primary_domains: dict[str, int] = defaultdict(lambda: 0)
        for domain in Domain.objects.raw(
            sql, [tuple(domain["tenant"].name for domain in self.initial_data)]
        ):
            if domain.is_primary:
                primary_domains[domain.tenant.name] += 1
        for domain in self.initial_data:
            primary_domains[domain["tenant"].name] += int(domain["is_primary"])
        for company, counter in primary_domains.items():
            if counter > 1:
                raise ValidationError(f"Company {company} already has a primary domain")
        return super().is_valid(raise_exception=raise_exception)


# pylint: disable=too-few-public-methods
class DomainSerializer(serializers.ModelSerializer):
    """
    Serializer for the Domain model
    """

    class Meta:
        """
        Metaclass for DomainSerializer
        """

        model = Domain
        fields = (
            "id",
            "domain",
            "created_at",
            "tenant",
            "is_primary",
        )
        read_only_fields = ("created_at", "id", "tenant")
        list_serializer_class = UniquenessListSerializer

    def validate_domain(self, value):  # noqa
        """
        Validate that the domain is given in the correct format
        """
        DomainFormatValidator(
            regex=getattr(
                settings,
                "VALID_DOMAINS_REGEX",
                r"^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}$",
            ),
            message="Invalid domain format",
        )(value)
        return value
