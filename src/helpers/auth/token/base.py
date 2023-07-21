from datetime import timedelta

from django.conf import settings
from django.dispatch import Signal
from rest_framework_simplejwt.tokens import Token

token_generated = Signal()


class BaseToken(Token):
    token_type = None
    lifetime = None
    api_settings = settings.SIMPLE_JWT
    company_model = api_settings.get("COMPANY_MODEL", "organization.Company")
    user_model = api_settings.get("USER_MODEL", "users.User")

    @classmethod
    def for_user(cls, user, should_signal=True):
        user_id = getattr(user, cls.api_settings["USER_ID_FIELD"])
        if not isinstance(user_id, int):
            user_id = str(user_id)

        token = cls()
        token[cls.api_settings["USER_ID_CLAIM"]] = user_id
        token["intended_for"] = "user.User"

        # Signal that the activation token has been generated
        # for the given user
        if should_signal:
            cls.signal(token)
        return token

    @classmethod
    def for_company(cls, company, should_signal=True):
        company_id = getattr(company, cls.api_settings["COMPANY_ID_CLAIM"])
        if not isinstance(company_id, int):
            company_id = str(company_id)
        token = cls()
        token[cls.api_settings["COMPANY_ID_CLAIM"]] = company_id
        token["intended_for"] = "organization.Company"

        # Signal that the activation token has been generated
        # for the given company
        if should_signal:
            cls.signal(token)
        return token

    def signal(self):
        token_generated.send(sender=self.__class__, token=self)
