from abc import ABC
from rest_framework import serializers

from services.country.models.country import Country
from helpers.validators.list_unique import ListUniqueValidator


class UniquenessListSerializer(serializers.ListSerializer, ABC):
    """
    List serializer that checks for uniqueness of the given field
    """

    validators = [ListUniqueValidator(unique_field_names=["email", "name"])]


class CountrySerializer(serializers.ModelSerializer):
    """
    Serializer for the Country model
    """

    # One country can have up to 3 domains
    primary_domain = serializers.CharField(max_length=200)

    class Meta:
        """
        Metaclass for CountrySerializer
        """

        model = Country
        fields = (
            "id",
            "name",
            "primary_domain",
        )
        read_only_fields = ("id", "domains")
        write_only_fields = ("primary_domain",)
        list_serializer_class = UniquenessListSerializer

    def create(self, validated_data):
        """
        Create a new country
        and assign schema name to it
        using the country name
        """
        validated_data["schema_name"] = validated_data["name"]
        primary_domain = validated_data.pop("primary_domain")
        country = Country.objects.create(**validated_data)
        country.set_primary_domain(primary_domain)
        return country
