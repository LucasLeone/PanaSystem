"""Users views."""

# Django
from django.contrib.auth import authenticate, get_user_model

# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# Serializers
from panasystem.users.serializers import UserLoginSerializer, UserModelSerializer

User = get_user_model()

class UsersViewSet(viewsets.GenericViewSet):
    """Users view set."""

    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated], url_path='logout')
    def logout(self, request):
        """User log out."""
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"success": True, "detail": "Logged out!"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Token not found!"}, status=status.HTTP_400_BAD_REQUEST)
