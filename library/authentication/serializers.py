from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser instances.
    """
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    middle_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    role = serializers.CharField(required=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "password",
            "created_at",
            "updated_at",
            "role",
            "is_active",
            "is_staff",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        """
        Create a new CustomUser instance with a hashed password.
        """
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):
        """
        Update an existing CustomUser instance.
        Password is handled separately and stored in a hashed format.
        """
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()

        return instance
