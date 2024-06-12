"""Connect to API for tests."""

# Pytest
import pytest

# Django
from django.contrib.auth import get_user_model

# Django REST Framework
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    """Connect to API using JWT authentication."""
    
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='testpassword')
    response = client.post('/api/v1/users/login/', {'username': 'testuser', 'password': 'testpassword'}, format='json')
    assert response.status_code == 201, "Login failed, unable to retrieve tokens"
    
    access_token = response.data['access']
    refresh_token = response.data['refresh']
    
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    
    # Return both client and tokens for testing logout
    return client, refresh_token