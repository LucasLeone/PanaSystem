"""Test brands."""

# Pytest
import pytest

# Django REST Framework
from rest_framework import status

# Models
from panasystem.products.models import Brand

# Serializers
from panasystem.products.serializers import BrandSerializer

# Utils
from panasystem.utils.connect_api_tests import api_client


@pytest.mark.django_db
def test_brand_creation():
    """
    Test the creation of a Brand model instance.
    
    Ensures that a Brand object is created with the expected attributes.
    """
    brand = Brand.objects.create(name="BrandX", description="BrandX products")
    assert brand.name == "BrandX"
    assert brand.description == "BrandX products"
    assert str(brand) == "BrandX"


@pytest.mark.django_db
def test_brand_serializer():
    """
    Test the serialization of a Brand model instance.
    
    Ensures that the BrandSerializer correctly serializes the Brand object.
    """
    brand = Brand(name="BrandX", description="BrandX products")
    serializer = BrandSerializer(brand)
    data = serializer.data
    assert data['name'] == "BrandX"
    assert data['description'] == "BrandX products"


@pytest.mark.django_db
def test_create_brand(api_client):
    """
    Test creating a brand via the API.
    
    Ensures that a brand is correctly created and saved to the database.
    """
    url = '/api/v1/product-brands/'
    data = {'name': 'BrandX', 'description': 'BrandX products'}
    response = api_client[0].post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Brand.objects.count() == 1
    assert Brand.objects.get().name == 'BrandX'


@pytest.mark.django_db
def test_list_brands(api_client):
    """
    Test listing all brands via the API.
    
    Ensures that the list of brands is retrieved correctly.
    """
    Brand.objects.create(name="BrandX", description="BrandX products")
    Brand.objects.create(name="BrandY", description="BrandY products")
    url = '/api/v1/product-brands/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_update_brand(api_client):
    """
    Test updating a brand via the API.
    
    Ensures that a brand's details can be updated correctly.
    """
    brand = Brand.objects.create(name="BrandX", description="BrandX products")
    url = f'/api/v1/product-brands/{brand.id}/'
    data = {'name': 'BrandX Updated', 'description': 'BrandX updated products'}
    response = api_client[0].put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    brand.refresh_from_db()
    assert brand.name == 'BrandX Updated'
    assert brand.description == 'BrandX updated products'


@pytest.mark.django_db
def test_delete_brand(api_client):
    """
    Test deleting a brand via the API.
    
    Ensures that a brand can be deleted correctly.
    """
    brand = Brand.objects.create(name="BrandX", description="BrandX products")
    url = f'/api/v1/product-brands/{brand.id}/'
    response = api_client[0].delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Brand.objects.count() == 0


@pytest.mark.django_db
def test_retrieve_brand(api_client):
    """
    Test retrieving a single brand via the API.
    
    Ensures that a brand's details can be retrieved correctly by its ID.
    """
    brand = Brand.objects.create(name="BrandX", description="BrandX products")
    url = f'/api/v1/product-brands/{brand.id}/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == "BrandX"
    assert response.data['description'] == "BrandX products"