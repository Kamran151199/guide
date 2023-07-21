from collections import Counter
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class ListUniqueValidator:
    """
    Validator checking that the list of
    items does not contain duplicate values
    for the given field names.
    """

    message = _("This field must be unique.")

    def __init__(self, unique_field_names):
        self.unique_field_names = unique_field_names

    @staticmethod
    def has_duplicates(counter):
        """
        Check if a counter has duplicates
        """
        return any((count for count in counter.values() if count > 1))

    def __call__(self, value):
        field_counters = {
            field_name: Counter(
                item[field_name] for item in value if field_name in item
            )
            for field_name in self.unique_field_names
        }
        has_duplicates = any(
            (
                ListUniqueValidator.has_duplicates(counter)
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
