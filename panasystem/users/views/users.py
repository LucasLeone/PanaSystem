"""Users views."""

# Django
from django.contrib.auth import get_user_model

# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

# Serializers
from panasystem.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserCreateSerializer,
)
from panasystem.users.models import BlacklistedAccessToken


User = get_user_model()


class UsersViewSet(viewsets.GenericViewSet):
    """
    Users view set.

    Provides the following actions:
    - User login.
    - User logout (authenticated only).
    - Create a new user (admin only).
    - List all users (admin only).
    """

    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        """
        User sign in.

        Expects 'username' and 'password' in the request data.
        Returns the user's data along with an access and refresh token upon successful login.
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.context["user"]

        refresh = RefreshToken.for_user(user)
        data = {
            "user": UserModelSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="logout",
    )
    def logout(self, request):
        """
        User log out.

        Invalidates the refresh token to log out the user.
        Returns a success message upon successful logout.
        """
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required for logout."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Add access token to the blacklist
            access_token = request.auth
            if access_token:
                BlacklistedAccessToken.objects.create(token=str(access_token))

            return Response(
                {"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK
            )
        except TokenError:
            return Response(
                {"detail": "Invalid or expired token!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsAdminUser],
        url_path="create",
    )
    def create_user(self, request):
        """
        Create a new user (Admin only).

        Only accessible by admin users.
        """
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserModelSerializer(user).data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated, IsAdminUser],
        url_path="list",
    )
    def list_users(self, request):
        """
        List all users (Admin only).

        Only accessible by admin users.
        """
        users = User.objects.all()
        serializer = UserModelSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)