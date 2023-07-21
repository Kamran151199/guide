from rest_framework import serializers


class AddOrRemoveSerializerMixin:
    """
    Mixin which provides update, validate duplicate methods
    """

    def __new__(
        cls,
        field_in_context,
    ):
        """
        This is a factory method which returns a new class with the
        required methods (to avoid code duplication).
        """

        if not field_in_context:
            raise serializers.ValidationError("Field is required")

        class MixinSerializer:
            def update(self, _, validated_data):
                return self.create(validated_data)

            def validate(self, attrs):
                if not self.context.get(field_in_context, None):
                    raise serializers.ValidationError(
                        f"{field_in_context.capitalize()} must be provided in the context."
                    )
                return attrs

        return MixinSerializer
