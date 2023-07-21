"""
Country entities
Each country is a tenant in the system
"""

import uuid

from django.db import models
from django_tenants.models import TenantMixin
from rest_framework.exceptions import ValidationError

from services.country.serializers.domain import DomainSerializer


class Country(TenantMixin):
    """
    It contains the schema name and
    other information about the tenant.
    This is required for separation of data between countries.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True, help_text="Name of the country")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    auto_create_schema = True

    def __str__(self) -> str:
        """
        Returns the name of the company
        """
        return str(self.name)

    def _set_domain(self, domain_url: str, is_primary: bool = False):
        """
        Set the domain for the company
        The following steps are performed:
        1. Create a serializer for the domain
        2. Validate the serializer
           2.1. If the domain is primary, check if the domain already exists
           2.2. If the domain is already assigned to another company, raise an error
           2.3. If the count of domains for the company is more than possible, raise an error
        3. Save the domain
        """
        domain = DomainSerializer(
            data={"domain": domain_url, "is_primary": is_primary, "tenant": self}
        )
        domain.is_valid(raise_exception=True)
        domain.save(tenant=self)
        return domain

    def set_primary_domain(self, domain_url: str):
        """
        Set the primary domain for the company
        The following steps are performed:
        1. Check if the primary domain for this company already exists
            1.1. If the primary domain exists, raise an error
            1.2. If the primary domain does not exist, set the primary domain using the _set_domain method
        This method calls the _set_domain method to make sure
        that the required validations are performed
        """
        if self.domains.filter(
                is_primary=True
        ).exists():  # noqa  # pylint: disable=no-member
            raise ValidationError("Primary domain already exists")
        domain = self._set_domain(domain_url, is_primary=True)
        return domain
