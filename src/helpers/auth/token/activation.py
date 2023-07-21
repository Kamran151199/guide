from datetime import timedelta

from django.conf import settings
from django.dispatch import Signal

from helpers.auth.token.base import BaseToken  # noqa: F401

activation_token_generated = Signal()


class ActivationToken(BaseToken):
    """
    This class is used to generate activation
    tokens for users and companies.
    """

    token_type = "activation"
    api_settings = settings.SIMPLE_JWT
    lifetime = api_settings.get("ACTIVATION_TOKEN_LIFETIME", timedelta(minutes=15))

    def signal(self):
        activation_token_generated.send(sender=self.__class__, token=self)
        super().signal()
