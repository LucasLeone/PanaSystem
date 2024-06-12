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

    class Meta:
        """Meta class."""

        model = User
        fields = (
            'username',
            'name',
            'email',
        )


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login request data.
    """

    username = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        self.context['user'] = user
        return data

    def create(self, validated_data):
        """Generate JWT token."""
        user = self.context['user']
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return user, access_token, refresh_token