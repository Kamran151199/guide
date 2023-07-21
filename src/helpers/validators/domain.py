import re

from rest_framework.serializers import ValidationError


class DomainFormatValidator:
    """
    Validate that the domain is
    given in the correct format
    """

    def __init__(self, regex, message):
        """
        :param regex: The regex to validate the domain
        :param message: The error message to display
        """
        self.regex = regex
        self.message = message

    def __call__(self, value):
        """
        :param value: The domain to validate
        """
        if not re.compile(self.regex).fullmatch(value):
            raise ValidationError(self.message)
