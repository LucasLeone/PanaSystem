"""Test categories."""

# Pytest
import pytest

# Django REST Framework
from rest_framework import status

# Models
from panasystem.products.models import Category

# Serializers
from panasystem.products.serializers import CategorySerializer

# Utils
from panasystem.utils.connect_api_tests import api_client


@pytest.mark.django_db
def test_category_creation():
    """
    Test the creation of a Category model instance.
    
    Ensures that a Category object is created with the expected attributes.
    """
    category = Category.objects.create(name="Bakery", description="Bakery products")
    assert category.name == "Bakery"
    assert category.description == "Bakery products"
    assert str(category) == "Bakery"


@pytest.mark.django_db
def test_category_serializer():
    """
    Test the serialization of a Category model instance.
    
    Ensures that the CategorySerializer correctly serializes the Category object.
    """
    category = Category(name="Bakery", description="Bakery products")
    serializer = CategorySerializer(category)
    data = serializer.data
    assert data['name'] == "Bakery"
    assert data['description'] == "Bakery products"


@pytest.mark.django_db
def test_create_category(api_client):
    """
    Test creating a category via the API.
    
    Ensures that a category is correctly created and saved to the database.
    """
    url = '/api/v1/product-categories/'
    data = {'name': 'Bakery', 'description': 'Bakery products'}
    response = api_client[0].post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Category.objects.count() == 1
    assert Category.objects.get().name == 'Bakery'


@pytest.mark.django_db
def test_list_categories(api_client):
    """
    Test listing all categories via the API.
    
    Ensures that the list of categories is retrieved correctly.
    """
    Category.objects.create(name="Bakery", description="Bakery products")
    Category.objects.create(name="Dairy", description="Dairy products")
    url = '/api/v1/product-categories/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_update_category(api_client):
    """
    Test updating a category via the API.
    
    Ensures that a category's details can be updated correctly.
    """
    category = Category.objects.create(name="Bakery", description="Bakery products")
    url = f'/api/v1/product-categories/{category.id}/'
    data = {'name': 'Baked Goods', 'description': 'All baked goods'}
    response = api_client[0].put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    category.refresh_from_db()
    assert category.name == 'Baked Goods'
    assert category.description == 'All baked goods'


@pytest.mark.django_db
def test_delete_category(api_client):
    """
    Test deleting a category via the API.
    
    Ensures that a category can be deleted correctly.
    """
    category = Category.objects.create(name="Bakery", description="Bakery products")
    url = f'/api/v1/product-categories/{category.id}/'
    response = api_client[0].delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Category.objects.count() == 0


@pytest.mark.django_db
def test_retrieve_category(api_client):
    """
    Test retrieving a single category via the API.
    
    Ensures that a category's details can be retrieved correctly by its ID.
    """
    category = Category.objects.create(name="Bakery", description="Bakery products")
    url = f'/api/v1/product-categories/{category.id}/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == "Bakery"
    assert response.data['description'] == "Bakery products"