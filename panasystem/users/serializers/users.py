"""Users serializers."""

# Django
from django.contrib.auth import authenticate

# Django REST Framework
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

# Models
from panasystem.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    groups = serializers.SerializerMethodField()

    class Meta:
        """Meta class."""

        model = User
        fields = (
            "username",
            "name",
            "email",
            "groups",
        )

    def get_groups(self, obj):
        """Get the names of the groups the user belongs to."""
        return [group.name for group in obj.groups.all()]


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login request data.
    """

    username = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        self.context["user"] = user
        return data

    def create(self, validated_data):
        """Generate JWT token."""
        user = self.context["user"]
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return user, access_token, refresh_token


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user."""

    class Meta:
        model = User
        fields = ("username", "password", "name", "email")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            name=validated_data.get("name", ""),
            email=validated_data.get("email", ""),
        )
        return user
