from rest_framework import serializers

from .models import Category, Location


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "created_at"]
        read_only_fields = ["id", "created_at"]


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class LocationSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Location
        fields = [
            "id",
            "name",
            "description",
            "category",
            "address",
            "latitude",
            "longitude",
            "author",
            "created_at",
            "updated_at",
            "is_deleted",
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at"]
