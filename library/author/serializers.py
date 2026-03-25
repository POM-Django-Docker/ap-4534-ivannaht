from rest_framework import serializers
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author instances.
    """
    class Meta:
        model = Author
        fields = [
            "id",
            "name",
            "surname",
            "patronymic",
            "books",
        ]
        read_only_fields = ["id"]
