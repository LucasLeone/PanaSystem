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
    user = User.objects.create_user(
        username="testuser123",
        password="testpassword",
        name="Test User",
        email="test@example.com",
    )
    assert user.username == "testuser123"
    assert user.check_password("testpassword")
    assert user.name == "Test User"
    assert user.email == "test@example.com"


@pytest.mark.django_db
def test_user_model_serializer():
    """
    Test the serialization of a User model instance.

    Ensures that the UserModelSerializer correctly serializes the User object.
    """
    user = User.objects.create_user(
        username="testuser123",
        password="testpassword",
        name="Test User",
        email="test@example.com",
    )
    serializer = UserModelSerializer(user)
    data = serializer.data
    assert data["username"] == "testuser123"
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"


@pytest.mark.django_db
def test_user_login(api_client):
    """
    Test user login via the API.

    Ensures that a user can log in with valid credentials and receive an access token.
    """
    User.objects.create_user(
        username="testuser123",
        password="testpassword",
        name="Test User",
        email="test@example.com",
    )
    url = "/api/v1/users/login/"
    data = {"username": "testuser123", "password": "testpassword"}
    response = api_client[0].post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert "access" in response.data
    assert response.data["user"]["username"] == "testuser123"


@pytest.mark.django_db
def test_user_logout(api_client):
    """
    Test user logout via the API.

    Ensures that a user can log out and receive a confirmation message.
    """
    user = User.objects.create_user(username="testuser123", password="testpassword")
    url = "/api/v1/users/logout/"
    refresh_token = api_client[1]
    response = api_client[0].post(url, {"refresh": refresh_token}, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["detail"] == "Logged out!"


@pytest.mark.django_db
def test_admin_can_create_user(api_client):
    """
    Test that only admin users can create new users via the API.

    Ensures that a user cannot create a new user unless they are an admin.
    """
    # Create a normal user
    user = User.objects.create_user(
        username="normaluser",
        password="testpassword",
        name="Normal User",
        email="normal@example.com",
    )
    # Create an admin user
    admin_user = User.objects.create_superuser(
        username="adminuser",
        password="testpassword",
        name="Admin User",
        email="admin@example.com",
    )

    create_url = "/api/v1/users/create/"

    # Login as normal user
    login_url = "/api/v1/users/login/"
    login_data = {"username": "normaluser", "password": "testpassword"}
    normal_login_response = api_client[0].post(login_url, login_data, format="json")
    normal_token = normal_login_response.data["access"]

    # Login as admin user
    admin_login_data = {"username": "adminuser", "password": "testpassword"}
    admin_login_response = api_client[0].post(
        login_url, admin_login_data, format="json"
    )
    admin_token = admin_login_response.data["access"]

    # Attempt to create a user as normal user
    normal_client = api_client[0]
    normal_client.credentials(HTTP_AUTHORIZATION=f"Bearer {normal_token}")
    create_data = {
        "username": "newuser",
        "password": "newpassword",
        "name": "New User",
        "email": "new@example.com",
    }
    response = normal_client.post(create_url, create_data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Attempt to create a user as admin user
    admin_client = api_client[0]
    admin_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = admin_client.post(create_url, create_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == "newuser"
    assert response.data["name"] == "New User"
    assert response.data["email"] == "new@example.com"


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
    user = User.objects.create_user(
        username="testuser123",
        password="testpassword",
        name="Test User",
        email="test@example.com",
    )
    assert user.username == "testuser123"
    assert user.check_password("testpassword")
    assert user.name == "Test User"
    assert user.email == "test@example.com"


@pytest.mark.django_db
def test_user_model_serializer():
    """
    Test the serialization of a User model instance.

    Ensures that the UserModelSerializer correctly serializes the User object.
    """
    user = User.objects.create_user(
        username="testuser123",
        password="testpassword",
        name="Test User",
        email="test@example.com",
    )
    serializer = UserModelSerializer(user)
    data = serializer.data
    assert data["username"] == "testuser123"
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"


@pytest.mark.django_db
def test_user_login(api_client):
    """
    Test user login via the API.

    Ensures that a user can log in with valid credentials and receive an access token.
    """
    User.objects.create_user(
        username="testuser123",
        password="testpassword",
        name="Test User",
        email="test@example.com",
    )
    url = "/api/v1/users/login/"
    data = {"username": "testuser123", "password": "testpassword"}
    response = api_client[0].post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert "access" in response.data
    assert response.data["user"]["username"] == "testuser123"


@pytest.mark.django_db
def test_user_logout(api_client):
    """
    Test user logout via the API.

    Ensures that a user can log out and receive a confirmation message.
    """
    user = User.objects.create_user(username="testuser123", password="testpassword")
    url = "/api/v1/users/logout/"
    refresh_token = api_client[1]
    response = api_client[0].post(url, {"refresh": refresh_token}, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["detail"] == "Logged out!"


@pytest.mark.django_db
def test_admin_can_create_user(api_client):
    """
    Test that only admin users can create new users via the API.

    Ensures that a user cannot create a new user unless they are an admin.
    """
    # Create a normal user
    user = User.objects.create_user(
        username="normaluser",
        password="testpassword",
        name="Normal User",
        email="normal@example.com",
    )
    # Create an admin user
    admin_user = User.objects.create_superuser(
        username="adminuser",
        password="testpassword",
        name="Admin User",
        email="admin@example.com",
    )

    create_url = "/api/v1/users/create/"

    # Login as normal user
    login_url = "/api/v1/users/login/"
    login_data = {"username": "normaluser", "password": "testpassword"}
    normal_login_response = api_client[0].post(login_url, login_data, format="json")
    normal_token = normal_login_response.data["access"]

    # Login as admin user
    admin_login_data = {"username": "adminuser", "password": "testpassword"}
    admin_login_response = api_client[0].post(
        login_url, admin_login_data, format="json"
    )
    admin_token = admin_login_response.data["access"]

    # Attempt to create a user as normal user
    normal_client = api_client[0]
    normal_client.credentials(HTTP_AUTHORIZATION=f"Bearer {normal_token}")
    create_data = {
        "username": "newuser",
        "password": "newpassword",
        "name": "New User",
        "email": "new@example.com",
    }
    response = normal_client.post(create_url, create_data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Attempt to create a user as admin user
    admin_client = api_client[0]
    admin_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = admin_client.post(create_url, create_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == "newuser"
    assert response.data["name"] == "New User"
    assert response.data["email"] == "new@example.com"


@pytest.mark.django_db
def test_admin_can_list_users(api_client):
    """
    Test that only admin users can list all users via the API.

    Ensures that a user cannot list users unless they are an admin.
    """
    # Create a normal user
    user = User.objects.create_user(
        username="normaluser",
        password="testpassword",
        name="Normal User",
        email="normal@example.com",
    )
    # Create an admin user
    admin_user = User.objects.create_superuser(
        username="adminuser",
        password="testpassword",
        name="Admin User",
        email="admin@example.com",
    )

    list_url = "/api/v1/users/list/"

    # Login as normal user
    login_url = "/api/v1/users/login/"
    login_data = {"username": "normaluser", "password": "testpassword"}
    normal_login_response = api_client[0].post(login_url, login_data, format="json")
    normal_token = normal_login_response.data["access"]

    # Login as admin user
    admin_login_data = {"username": "adminuser", "password": "testpassword"}
    admin_login_response = api_client[0].post(
        login_url, admin_login_data, format="json"
    )
    admin_token = admin_login_response.data["access"]

    # Attempt to list users as normal user
    normal_client = api_client[0]
    normal_client.credentials(HTTP_AUTHORIZATION=f"Bearer {normal_token}")
    response = normal_client.get(list_url, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Attempt to list users as admin user
    admin_client = api_client[0]
    admin_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    response = admin_client.get(list_url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert len(response.data) > 0  # Assuming there are users in the database
