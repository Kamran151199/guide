"""
This module contains the User views
"""

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, DjangoObjectPermissions, IsAuthenticated
from rest_framework.response import Response

from helpers.auth.custom_jwt import JWTAuth
from helpers.mixins.permissions.policy import PermissionPolicyMixin
from helpers.permissions.model import ModelPermissions
from services.user.filters.user import UserFilterSet
from services.user.models.user import User
from services.user.serializers.user import (UserPasswordResetSerializer)
from services.user.serializers.user import (
    UserSerializer,
    UserActivationSerializer,
)


class UserViewSet(PermissionPolicyMixin, viewsets.ModelViewSet):
    """
    API endpoint for User model.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuth]

    permission_classes = [ModelPermissions, DjangoObjectPermissions]
    permission_classes_by_action = {
        "create": [AllowAny],
        "activate": [AllowAny],
        "resend_activation": [AllowAny],
        "reset_password": [AllowAny],
        "resend_verification": [AllowAny],
        "verify": [AllowAny],
    }

    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    search_fields = ("username", "email", "first_name", "last_name")
    filterset_class = UserFilterSet

    pagination_class = PageNumberPagination
    pagination_class.page_size = 100
    pagination_class.page_size_query_param = "page_size"

    # override the delete method to restrict self-deletion
    def destroy(self, request, *args, **kwargs):
        """
        Override the default delete method
        to restrict self-deletion.
        """
        instance = self.get_object()
        if instance == request.user:
            raise ValidationError("You cannot delete yourself.")
        return super().destroy(request, *args, **kwargs)

    @method_decorator(never_cache)
    @action(methods=["GET"], detail=False, url_path="me", url_name="me")
    def get_me(
            self, request, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """
        Get the current user.
        """
        user = self.get_serializer(request.user)
        return Response(data=user.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """
        Override the default create method
        to set the request to the serializer context.
        """
        self.get_serializer_context()["request"] = self.request
        return super().perform_create(serializer)

    @swagger_auto_schema(
        operation_summary="User email verification",
        operation_description="Verify registration token sent to user email",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["verification_token"],
            properties={"verification_token": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        responses={
            200: openapi.Response(
                description="User email verified",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "activation_token": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                    required=["activation_token"],
                ),
            ),
            400: openapi.Response(
                description="Invalid verification token",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                    required=["detail"],
                ),
            ),
        },
        methods=["POST"],
    )
    @action(methods=["POST"], detail=False, url_path="verify", url_name="verify")
    def verify(
            self, request, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """
        Verify the user email address using the verification token
        sent to the user's email address.
        The following steps are performed:
        1. Get the user using the verification token
        2. Verify the user's email address
        3. Return the activation code
        """
        verification_code = request.data.get("verification_token")
        user = JWTAuth().get_user(
            JWTAuth().get_validated_token(verification_code, purpose="verification"),
            force_unverified=True,
            force_inactive=True,
        )

        if user:
            if user.is_verified:
                raise ValidationError(detail="User is already verified.")
            activation_token = user.verify()
            return Response(
                data={"activation_token": str(activation_token)},
                status=status.HTTP_200_OK,
            )
        raise ValidationError(detail="Invalid verification token.")

    @swagger_auto_schema(
        operation_summary="User activation",
        operation_description="Activate user using activation code",
        responses={
            200: openapi.Response(
                description="User activated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=["message"],
                    properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
            400: openapi.Response(
                description="Invalid activation code",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=["detail"],
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        },
        methods=["POST"],
    )
    @action(
        methods=["POST"],
        detail=False,
        serializer_class=UserActivationSerializer,
        url_path="activate",
        url_name="activate",
    )
    def activate(
            self, request, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """
        Activate the user using the activation token sent to the user's email address.
        The following steps are performed:
        1. Get the user using the activation token
        2. Activate the user
        3. Set the user's password
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.save():
            return Response(
                data={"message": "User activated successfully."},
                status=status.HTTP_200_OK,
            )
        raise ValidationError(detail="Invalid activation code.")

    @swagger_auto_schema(
        operation_summary="Resend verification email",
        operation_description="Resend verification email to user email",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email"],
            properties={"email": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        methods=["POST"],
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="resend-verification",
        url_name="resend-verification",
    )
    def resend_verification(
            self, request, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """
        User email verification is required before activating the user.
        If the user email verification link expires, the root user can request
        for a new verification link to be sent to the user's email address.
        The following steps are performed:
        1. Get the user using the user email address
        2. Check if the user is already verified:
            2.1 If the user is already verified, return an error
            2.2 If the user is not verified, send the verification
            email to the user's email address (background task)
        """
        email = request.data.get("email")
        user = User.objects.filter(email=email)
        if not user.exists():
            raise ValidationError(detail="User with provided email is not registered.")
        user = user.first()
        if user.is_verified:
            raise ValidationError(detail="User is already verified.")
        user.create_token(
            purpose="verification",
            should_signal=True,
        )
        return Response(
            data={"message": "Verification email has been sent to your email address."},
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_summary="Resend activation email",
        operation_description="Resend activation email to user email",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email"],
            properties={"email": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        methods=["POST"],
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="resend-activation",
        url_name="resend-activation",
    )
    def resend_activation(
            self, request, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """
        User activation is required before the user can join the company.
        If the user activation link expires, the company's root user can request
        for a new activation link to be sent to the user's email address.
        The following steps are performed:
        1. Get the user using the user's email address
        2. Check if the user is already activated:
            2.1 If the user is already activated, return an error
            2.2 If the user is not activated, send the activation email
            to the user's email address (background task)
        """
        email = request.data.get("email")
        user = User.objects.filter(email=email)
        if not user.exists():
            raise ValidationError(detail="User with provided email is not registered.")
        user = user.first()
        if user.is_active:
            raise ValidationError(detail="User is already active.")
        user.create_token(purpose="activation", should_signal=True)
        return Response(
            data={"message": "Activation email has been sent to your email address."},
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_summary="Request password reset",
        operation_description="Request password reset for user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
        ),
        responses={
            200: openapi.Response(
                description="Password reset email sent",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=["message"],
                    properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
            400: openapi.Response(
                description="Invalid email",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=["detail"],
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        },
    )
    @action(methods=["POST"], detail=True, url_path="request_password_reset")
    def request_password_reset(
            self, request, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """
        Request password reset
        """
        user = self.get_object()
        user.create_token(purpose="password_reset", should_signal=True)
        return Response(
            data={
                "message": "Password reset email has been sent to your email address."
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_summary="Forgot password request",
        operation_description="Forgot password request",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email"],
            properties={"email": openapi.Schema(type=openapi.TYPE_STRING)},
        ),
        responses={
            200: openapi.Response(
                description="Password reset email sent",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=["message"],
                    properties={"message": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
            400: openapi.Response(
                description="Invalid email",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=["detail"],
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        },
    )
    @action(methods=["POST"],
            detail=False,
            url_path="forgot_password",
            authentication_classes=[],
            permission_classes=[])
    def forgot_password(
            self, request, *args, **kwargs
    ):
        """
        Request forgot password
        """
        email = request.data.get("email")
        user = User.objects.filter(email=email)
        if not user.exists():
            raise ValidationError(detail="User with provided email is not registered.")
        user = user.first()
        user.create_token(purpose="password_reset", should_signal=True)
        return Response(
            data={
                "message": "Password reset email has been sent to your email address."
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_summary="Reset password",
        operation_description="Reset password for user",
        request_body=UserPasswordResetSerializer,
        responses={
            200: openapi.Response(
                description="Password reset successful",
                schema=UserSerializer,
            ),
            400: openapi.Response(
                description="Invalid password reset code",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=["detail"],
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        },
    )
    @action(
        methods=["POST"],
        detail=False,
        serializer_class=UserPasswordResetSerializer,
        authentication_classes=[],
        permission_classes=[],
        url_path="reset_password",
    )
    def reset_password(
            self, request, *args, **kwargs
    ):  # pylint: disable=unused-argument
        """
        Reset password
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"message": "Password reset successful."},
            status=status.HTTP_200_OK,
        )
