from django_filters import FilterSet

from services.user.models.user import User


class UserFilterSet(FilterSet):
    class Meta:
        model = User
        fields = {
            "username": ["exact", "contains", "icontains"],
            "first_name": ["exact", "contains", "icontains"],
            "last_name": ["exact", "contains", "icontains"],
            "email": ["exact", "contains", "icontains"],
            "is_active": ["exact"],
            "is_verified": ["exact"],
            "is_staff": ["exact"],
            "company__name": ["exact", "contains", "icontains"],
            "groups": ["exact", "contains", "icontains"],
        }
