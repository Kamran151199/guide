"""
Domain entities
Domain is an identifier for a country
"""
import uuid

from django.db import models
from django_tenants.models import DomainMixin
from rest_framework.exceptions import ValidationError


class Domain(DomainMixin):
    """
    Domain entity for a country
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Returns the domain name
        """
        return str(self.domain)

    def validate_unique(self, exclude=None):
        """
        Validate that the domain is unique
        """
        if self.is_primary:
            primary_domain = Domain.objects.filter(is_primary=True, tenant=self.tenant)
            if primary_domain.exists() and primary_domain.first().id != self.id:
                raise ValidationError(
                    f"There is already a primary domain for {self.tenant.name}"
                )
        return super().validate_unique(exclude)

    def save(self, *args, **kwargs):
        """
        Save the domain
        """
        self.validate_unique()
        return super().save(*args, **kwargs)
