from helpers.auth.token import PasswordResetToken
from helpers.auth.token.password_reset import password_reset_token_generated
from helpers.auth.token.verification import (
    VerificationToken,
    verification_token_generated,
)
from helpers.auth.token.activation import ActivationToken, activation_token_generated

from services.mailer.tasks.security import send_email
from services.mailer.utils.security import make_security_email_payload


def send_security_email(sender, token, **kwargs):
    """
    This signal is triggered when a verification token is generated.
    It sends the verification token to the user.
    """
    send_email.delay(**make_security_email_payload(token))


activation_token_generated.connect(send_security_email, sender=ActivationToken)
verification_token_generated.connect(send_security_email, sender=VerificationToken)
password_reset_token_generated.connect(send_security_email, sender=PasswordResetToken)
