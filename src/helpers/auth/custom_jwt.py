"""
JWT uses this rule to return the user object. We can modify
it for our need (e.g. is_verified=True)
"""
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import APISettings, IMPORT_STRINGS

from helpers.auth.token import ActivationToken, VerificationToken, PasswordResetToken

# We need to provide our OWN DEFAULTS
# because if the custom keys which we added are not provided
# in the DEFAULTS, overriding SIMPLE_JWT settings will
# include our custom keys in the settings.
# For more information, please dive into the source code of
# rest_framework_simplejwt.settings.APISettings and
# rest_framework.settings.APISettings <- this is where the magic happens
api_settings = APISettings(
    getattr(settings, "SIMPLE_JWT", {}),
    getattr(settings, "SIMPLE_JWT", {}),
    IMPORT_STRINGS,
)


class JWTAuth(JWTAuthentication):
    """
    JWTAuth class is used to
    override the default JWTAuthentication class.
    """

    def __init__(self, *args, **kwargs):
        """
        Override the default __init__ method to
        set the company_model which
        is not provided by default.
        """
        super().__init__(*args, **kwargs)

    def get_validated_token(
            self,
            raw_token,
            purpose="authentication",
    ):
        """
        Override the default get_validated_token method to
        check if the token is valid or not for not only authentication
        purpose but also for activation/verification/password-reset purposes.
        """
        match purpose:
            case "authentication":
                try:
                    return super().get_validated_token(raw_token)
                except InvalidToken as exc:
                    raise AuthenticationFailed(
                        detail=exc.detail.get("detail", exc.default_detail),
                        code=exc.detail.get("code", exc.default_code),
                    ) from exc
            case "activation":
                try:
                    return ActivationToken(token=raw_token)
                except TokenError as exc:
                    raise AuthenticationFailed(
                        detail=str(exc.args[0]),
                        code=str("invalid_token"),
                    ) from exc
            case "verification":
                try:
                    return VerificationToken(raw_token)
                except TokenError as exc:
                    raise AuthenticationFailed(
                        detail=exc.args[0],
                        code="invalid_token",
                    ) from exc
            case "password_reset":
                try:
                    return PasswordResetToken(raw_token)
                except TokenError as exc:
                    raise AuthenticationFailed(
                        detail=exc.args[0],
                        code="invalid_token",
                    ) from exc
            case _:
                raise AuthenticationFailed(
                    detail=_("Invalid purpose"),
                    code="invalid_purpose",
                )

    def get_user(
            self,
            validated_token,
            force_unverified=False,
            force_inactive=False,
    ):
        """
        Override the default get_user method.
        It adds the force_unverified and force_inactive parameters.

        :param validated_token: validated token
        :param force_unverified: if True, it will return the
            user even if it is not verified
        :param force_inactive: if True, it will return the
            user even if it is inactive
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError as exc:
            raise InvalidToken(
                detail=_("Token contained no recognizable user identification"),
                code="invalid_token",
            ) from exc

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist as exc:
            raise AuthenticationFailed(
                _("User not found"), code="user_not_found"
            ) from exc

        if not user.is_active and not force_inactive:
            raise AuthenticationFailed(
                detail="User is not active", code="user_inactive"
            )

        if not user.is_verified and not force_unverified:
            raise AuthenticationFailed(
                detail="User is not verified", code="not_verified"
            )
        return user


def custom_user_authentication_rule(user):
    """
     JWT uses this rule to return the user object.
     We can modify it for our need (e.g. is_verified=True)
    :param user:
    :return:
    """
    if user:
        if not user.is_verified:
            raise AuthenticationFailed(
                detail="User is not verified", code="not_verified"
            )
        if not user.is_active:
            raise AuthenticationFailed(
                detail="User is not active", code="user_inactive"
            )
    return user and user.is_active
