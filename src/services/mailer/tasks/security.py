from core.celery import app

from helpers.email.send import send_templated_email


@app.task
def send_email(
    data: dict,
    html_template_path,
    text_template_path,
    subject,
    recipient,
):
    """
    Send email to the given email address
    using the given template and data

    :param data: dict data to be used in the template
    (e.g. send_verification_email, send_activation_email, etc.)
    :param html_template_path: path to html template
    :param text_template_path: path to text template
    :param subject: email subject
    :param recipient: email address of recipient
    Make sure that the data is convertable to dict.
    """
    send_templated_email(
        data=data,
        html_template_path=html_template_path,
        text_template_path=text_template_path,
        subject=subject,
        recipient=recipient,
    )
