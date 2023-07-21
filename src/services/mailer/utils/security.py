from django.apps import apps
from django.conf import settings
from django_tenants.utils import tenant_context


def get_subdomain(domain: str) -> str:
    """
    This function returns the subdomain of a domain.
    """
    return domain.split(".")[0]


def append_subdomain(url: str, subdomain: str) -> str:
    """
    This function appends a subdomain to a url.
    """

    # Get the domain from the url.
    domain = url.split("//")[1].split("/")[0]
    # append the subdomain to the domain.
    with_subdomain = f"{subdomain}.{domain}"
    # append the domain to the url.
    url = url.replace(domain, with_subdomain)
    return url


def make_security_email_payload(
        token,
):
    """
    This signal is triggered when a verification token is generated.
    It sends the verification token to the user.
    """

    token_type = token["token_type"]
    intended_for = token["intended_for"]

    if model := apps.get_model(intended_for):
        instance = model.objects.get(id=token["id"])
        secret = str(token)

        html_template_path = SECURITY_EMAIL_TEMPLATES[intended_for][token_type]["html"]
        text_template_path = SECURITY_EMAIL_TEMPLATES[intended_for][token_type]["text"]
        subject = SECURITY_EMAIL_SUBJECTS[intended_for][token_type]
        recipient = instance.email

        data = instance.to_dict()
        data["token"] = secret
        if intended_for == "user.User":
            company = getattr(instance, "company", None)
            if not company:
                company = instance.invited_by.company
            with tenant_context(company):
                client_url = settings.CLIENT_URL
                client_subdomain = get_subdomain(
                    company.domains.first().domain
                )
                data["client_url"] = append_subdomain(client_url, client_subdomain)
        else:
            data["client_url"] = settings.CLIENT_URL

        return {
            "data": data,
            "html_template_path": html_template_path,
            "text_template_path": text_template_path,
            "subject": subject,
            "recipient": recipient,
        }


SECURITY_EMAIL_SUBJECTS = {
    "user.User": {
        "verification": "Verify your email address",
        "activation": "Activate your account",
        "password_reset": "Reset your password",
    },
}

SECURITY_EMAIL_TEMPLATES = {
    "user.User": {
        "verification": {
            "html": "security/user/verification/verification.html",
            "text": "security/user/verification/verification.txt",
        },
        "activation": {
            "html": "security/user/activation/activation.html",
            "text": "security/user/activation/activation.txt",
        },
        "password_reset": {
            "html": "security/user/password_reset/password_reset.html",
            "text": "security/user/password_reset/password_reset.txt",
        },
    },
}
