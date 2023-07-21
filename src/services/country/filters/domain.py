from django_filters import FilterSet

from services.country.models.domain import Domain


class DomainFilterSet(FilterSet):
    """
    FilterSet for Domain model.
    """

    class Meta:
        model = Domain
        fields = {
            "tenant__name": ["exact", "contains", "icontains"],
            "domain": ["exact", "contains", "icontains"],
            "created_at": ["exact", "lt", "lte", "gt", "gte"],
            "is_primary": ["exact"],
        }
