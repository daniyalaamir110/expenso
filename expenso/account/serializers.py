from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import (
    validate_password as validate_password_django,
)
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User create serializer
    """

    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        max_length=20,
    )
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "full_name",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
            "full_name": {"read_only": True},
        }

    def validate_password(self, password):
        validate_password_django(password)
        return password

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class ChangeEmailSerializer(serializers.ModelSerializer):
    """
    Change email serializer
    """

    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email"]
        extra_kwargs = {
            "email": {"required": True},
        }

    def validate_email(self, email):
        user = self.context["request"].user
        if user.email == email:
            raise serializers.ValidationError("Email is already the same.")
        return email
