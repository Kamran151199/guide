"""
This file is part of the Yoona.ai project.
It contains the logic for sending emails to users.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from services.user.models import User


@receiver(post_save, sender=User)
def manage_post_creation(
        sender: User,  # noqa: F841 pylint: disable=unused-argument
        instance: User,
        created: bool,
        **kwargs
):
    """
    This signal is triggered when a user is created.
    It creates a verification token for the user
    which in turn signals the creation of a verification email.
    """

    if created:
        instance.create_token(purpose="verification")
