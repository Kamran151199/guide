from collections import Counter
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class ListUniqueValueWith:
    """
    Validator checking that the list of
    items does not contain duplicate field of specific value
    for the given `with_field`.
    """

    message = _(
        "This field with specified value must be"
        " unique for the given (`with_field`) field."
    )

    def __init__(
        self, unique_field_names: list[str], value: any, with_field: str, message=None
    ):
        self.unique_field_names = unique_field_names
        self.value = value
        self.with_field = with_field
        self.message = message or self.message

    @staticmethod
    def has_duplicates(counter):
        """
        Check if a counter has duplicates
        """
        return any((count for count in counter.values() if count > 1))

    def __call__(self, value):
        """
        Check if the field value is unique for the given model
        Note that this validator has high complexity - O(n*m)
        where n is the number of items in the list and m is the number of
        unique field names. Use it only when you really have to.
        """
        field_counters = {
            field_name: Counter(
                (item[field_name], item[self.with_field])
                for item in value
                if field_name in item and item[field_name] == self.value
            )
            for field_name in self.unique_field_names
        }

        has_duplicates = any(
            (
                ListUniqueValueWith.has_duplicates(counter)
                for counter in field_counters.values()
            )
        )
        if has_duplicates:
            errors = []
            for item in value:
                error = {}
                for field_name in self.unique_field_names:
                    counter = field_counters[field_name]
                    if counter[item.get(field_name)] > 1:
                        error[field_name] = self.message
                errors.append(error)
            raise ValidationError(errors)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}"
            f"(unique_field_names={self.unique_field_names})>"
        )
