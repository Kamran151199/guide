from rest_framework import serializers

from services.user.models.user import User
from helpers.auth.custom_jwt import JWTAuth


class UserSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "phone_number",
            "is_active",
            "is_staff",
            "is_verified",
            'country'
        )
        read_only_fields = (
            "is_staff",
            "is_verified",
            'country',
            "is_active",
            "id",
        )

    def validate(self, attrs):
        country = getattr(self.context.get('request', {}), 'tenant', None)
        if not country:
            raise serializers.ValidationError("Country not found")
        attrs['country'] = country
        return attrs


class UserActivationSerializer(serializers.Serializer):
    """
    Serializer for the User model activation
    Used to activate a user account and set a password
    """

    password = serializers.CharField()
    password_confirmation = serializers.CharField()
    activation_token = serializers.CharField()

    def validate(self, data):
        jwt = JWTAuth()

        user = jwt.get_user(
            jwt.get_validated_token(
                raw_token=data["activation_token"],
                purpose="activation",
            ),
            force_inactive=True,
        )

        if not user:
            raise serializers.ValidationError("Invalid activation token")

        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError("Passwords don't match")
        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        user.activate(self.validated_data["password"])
        return True


class UserPasswordResetSerializer(serializers.Serializer):
    """
    Serializer for the User model password reset
    Used to reset a user account password
    """

    password = serializers.CharField()
    password_confirmation = serializers.CharField()
    reset_token = serializers.CharField()

    def validate(self, data):
        jwt = JWTAuth()

        user = jwt.get_user(
            jwt.get_validated_token(
                raw_token=data["reset_token"],
                purpose="password_reset",
            ),
            force_inactive=True,
        )

        if not user:
            raise serializers.ValidationError("Invalid reset token")

        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError("Passwords don't match")
        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["password"])
        user.save()
        return True
