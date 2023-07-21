from datetime import timedelta

from django.conf import settings
from django.dispatch import Signal

from helpers.auth.token.base import BaseToken  # noqa: F401

password_reset_token_generated = Signal()


class PasswordResetToken(BaseToken):
    """
    This class is used to generate activation
    tokens for users and companies.
    """

    token_type = "password_reset"
    api_settings = settings.SIMPLE_JWT
    lifetime = api_settings.get("PASSWORD_RESET_TOKEN_LIFETIME", timedelta(minutes=15))

    def signal(self):
        password_reset_token_generated.send(sender=self.__class__, token=self)
        super().signal()
