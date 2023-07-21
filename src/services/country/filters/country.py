from django_filters import FilterSet
from services.country.models.country import Country


class CountryFilterSet(FilterSet):
    """
    FilterSet for Country model.
    """

    class Meta:
        model = Country
        fields = {
            "name": ["exact", "contains", "icontains"],
            "created_at": ["exact", "lt", "lte", "gt", "gte"],
            "updated_at": ["exact", "lt", "lte", "gt", "gte"],
        }
