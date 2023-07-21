from datetime import timedelta

from django.conf import settings
from django.dispatch import Signal

from helpers.auth.token.base import BaseToken  # noqa: F401

verification_token_generated = Signal()


class VerificationToken(BaseToken):
    """
    This class is used to generate verification
    tokens for users and companies.
    """

    token_type = "verification"
    api_settings = settings.SIMPLE_JWT
    lifetime = api_settings.get("VERIFICATION_TOKEN_LIFETIME", timedelta(minutes=15))

    def signal(self):
        verification_token_generated.send(sender=self.__class__, token=self)
        super().signal()
