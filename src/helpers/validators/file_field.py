from django.conf import settings
from rest_framework.exceptions import ValidationError


class FileFieldValidator:
    def __init__(
        self,
        required: bool = True,
        max_size: int = getattr(settings, "MAX_FILE_SIZE", 10000000),
        allowed_types: list = getattr(
            settings, "ALLOWED_FILE_TYPES", ["*/*"]
        ),
    ):
        self.required = required
        self.max_size = max_size
        self.allowed_types = allowed_types

    def validate(self, value):
        if self.required and not value:
            raise ValidationError("File is required")
        if value.size > self.max_size:
            raise ValidationError(
                f"File size is too large. Max size is {self.max_size} bytes."
            )
        if value.content_type not in self.allowed_types and self.allowed_types != ["*/*"]:
            raise ValidationError(
                f"File type {value.content_type} is not allowed. Allowed types are {self.allowed_types}."
            )

    def __call__(self, value, *args, **kwargs):
        self.validate(value)
