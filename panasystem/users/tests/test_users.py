"""Test users."""

# Pytest
import pytest

# Django
from django.contrib.auth import get_user_model

# Django REST Framework
from rest_framework import status

# Serializers
from panasystem.users.serializers import UserModelSerializer

# Utils
from panasystem.utils.connect_api_tests import api_client


User = get_user_model()


@pytest.mark.django_db
def test_user_creation():
    """
    Test the creation of a User model instance.

    Ensures that a User object is created with the expected attributes and that the password is set correctly.
    """
    user = User.objects.create_user(username='testuser123', password='testpassword', name='Test User', email='test@example.com')
    assert user.username == 'testuser123'
    assert user.check_password('testpassword')
    assert user.name == 'Test User'
    assert user.email == 'test@example.com'


@pytest.mark.django_db
def test_user_model_serializer():
    """
    Test the serialization of a User model instance.

    Ensures that the UserModelSerializer correctly serializes the User object.
    """
    user = User.objects.create_user(username='testuser123', password='testpassword', name='Test User', email='test@example.com')
    serializer = UserModelSerializer(user)
    data = serializer.data
    assert data['username'] == 'testuser123'
    assert data['name'] == 'Test User'
    assert data['email'] == 'test@example.com'


@pytest.mark.django_db
def test_user_login(api_client):
    """
    Test user login via the API.

    Ensures that a user can log in with valid credentials and receive an access token.
    """
    User.objects.create_user(username='testuser123', password='testpassword', name="Test User", email='test@example.com')
    url = '/api/v1/users/login/'
    data = {
        'username': 'testuser123',
        'password': 'testpassword'
    }
    response = api_client[0].post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access' in response.data
    assert response.data['user']['username'] == 'testuser123'


@pytest.mark.django_db
def test_user_logout(api_client):
    """
    Test user logout via the API.

    Ensures that a user can log out and receive a confirmation message.
    """
    user = User.objects.create_user(username='testuser123', password='testpassword')
    url = '/api/v1/users/logout/'
    refresh_token = api_client[1]
    response = api_client[0].post(url, {'refresh': refresh_token}, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['detail'] == 'Logged out!'