
"""
This file is part of the Yoona.ai project.
It contains the utility functions for sending
different types of emails.
"""

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def send_email(
    subject: str, email_to: str, html_alternative: str, text_alternative: str
) -> None:
    """
    Send email to the given email address
    :param subject: Subject of the email
    :param email_to: Email address to send the email to
    :param html_alternative: HTML version of the email
    :param text_alternative: Text version of the email
    :return: None
    """
    msg = EmailMultiAlternatives(
        subject, text_alternative, settings.EMAIL_FROM, [email_to]
    )
    msg.attach_alternative(html_alternative, "text/html")
    msg.send(fail_silently=False)


def send_templated_email(
    data: dict,
    html_template_path: str,
    text_template_path: str,
    subject: str,
    recipient: str,
):
    """
    Send verification email to company email
    :param data: dict version of CompanyModel
    :param html_template_path: path to html template
    :param text_template_path: path to text template
    :param subject: email subject
    :param recipient: email address of recipient
    """

    html_template = get_template(html_template_path)
    text_template = get_template(text_template_path)

    html_alternative = html_template.render(data)
    text_alternative = text_template.render(data)
    send_email(subject, recipient, html_alternative, text_alternative)
