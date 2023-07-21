from uuid import uuid4

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from helpers.auth.token import (
    ActivationToken,
    PasswordResetToken,
    VerificationToken,
    BaseToken,
)


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(
            self,
            email: str,
            username: str,
            password: str,
            **extra_fields,
    ):
        """
        Create and save a User with the given email and password.

        :param email: User's email
        :param username: Name to be displayed.
        :param password: Password
        :param extra_fields: Any additional (optional) field.
        :return: CustomUser
        """

        if not (email and username):
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
            self, email: str, username: str, password: str, **extra_fields
    ):
        """
        Create and save a SuperUser with the given email and password.

        :param email: User's email
        :param username: Name to be displayed.
        :param password: Password
        :param extra_fields: Any additional (optional) field.
        :return: CustomUser
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(
            email=email, password=password, username=username, **extra_fields
        )


class User(AbstractUser):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)
    username = models.CharField(
        verbose_name=_("Username"), max_length=200, unique=False
    )
    email = models.EmailField(
        verbose_name=_("Email address"), unique=True, null=False, blank=False
    )
    password = models.CharField(
        verbose_name=_("Password"), max_length=255, null=True, blank=True
    )
    phone_number = models.CharField(
        verbose_name=_("Phone number"),
        unique=True,
        null=True,
        blank=True,
        max_length=15,
    )
    country = models.OneToOneField(
        "country.Country",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("Country"),
    )
    created_at = models.DateTimeField(verbose_name=_("Date joined"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Date updated"), blank=True,
                                      editable=False, auto_now=True)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        ...

    def __str__(self):
        return f"{self.username}({self.email})"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def create_token(
            self,
            purpose: str,
            should_signal: bool = True,
    ) -> BaseToken:
        """
        Creates a token for the user with the given purpose.
        """

        match purpose:
            case "activation":
                return ActivationToken.for_user(self, should_signal=should_signal)
            case "password_reset":
                return PasswordResetToken.for_user(self, should_signal=should_signal)
            case "verification":
                return VerificationToken.for_user(self, should_signal=should_signal)
            case _:
                raise ValueError(_("Invalid purpose."))

    def verify(self) -> ActivationToken:
        if self.is_verified:
            raise ValidationError(_("User is already verified."))

        with transaction.atomic():
            self.is_verified = True
            self.save()
            return self.create_token(purpose="activation", should_signal=False)

    def activate(self, password: str):
        """
        Activate the user.
        Activating user will do the following:
        1. Activate the user.
        2. Set the password.
        3. Add the user to the group.
        """

        if self.is_active:
            raise ValidationError(_("User is already active."))

        with transaction.atomic():
            self.is_active = True
            self.set_password(password)
            self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "phone_number": self.phone_number,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }