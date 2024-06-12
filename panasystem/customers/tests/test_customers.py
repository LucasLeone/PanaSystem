"""Test customers."""

# Pytest
import pytest

# Django REST Framework
from rest_framework import status

# Models
from panasystem.customers.models import Customer

# Serializers
from panasystem.customers.serializers import CustomerSerializer

# Utils
from panasystem.utils.connect_api_tests import api_client


@pytest.mark.django_db
def test_customer_creation():
    """
    Test the creation of a Customer model instance.
    
    Ensures that a Customer object is created with the expected attributes.
    """
    customer = Customer.objects.create(name="Alice", email="alice@example.com")
    assert customer.name == "Alice"
    assert customer.email == "alice@example.com"
    assert str(customer) == "Alice"


def test_customer_serializer():
    """
    Test the serialization of a Customer model instance.
    
    Ensures that the CustomerSerializer correctly serializes the Customer object.
    """
    customer = Customer(name="Bob", email="bob@example.com", city=Customer.CITY_ARROYO_CABRAL)
    serializer = CustomerSerializer(customer)
    data = serializer.data
    assert data['name'] == "Bob"
    assert data['email'] == "bob@example.com"
    assert data['city_display'] == "Arroyo Cabral"


@pytest.mark.django_db
def test_create_customer(api_client):
    """
    Test creating a customer via the API.
    
    Ensures that a customer is correctly created and saved to the database.
    """
    url = '/api/v1/customers/'
    data = {'name': 'Alice', 'email': 'alice@example.com'}
    response = api_client[0].post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Customer.objects.count() == 1
    assert Customer.objects.get().name == 'Alice'


@pytest.mark.django_db
def test_list_customers(api_client):
    """
    Test listing all customers via the API.
    
    Ensures that the list of customers is retrieved correctly.
    """
    Customer.objects.create(name="Alice", email="alice@example.com")
    Customer.objects.create(name="Bob", email="bob@example.com")
    url = '/api/v1/customers/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_update_customer(api_client):
    """
    Test updating a customer via the API.
    
    Ensures that a customer's details can be updated correctly.
    """
    customer = Customer.objects.create(name="Alice", email="alice@example.com")
    url = f'/api/v1/customers/{customer.id}/'
    data = {'name': 'Alice Smith', 'email': 'alice.smith@example.com'}
    response = api_client[0].put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    customer.refresh_from_db()
    assert customer.name == 'Alice Smith'
    assert customer.email == 'alice.smith@example.com'


@pytest.mark.django_db
def test_delete_customer(api_client):
    """
    Test deleting a customer via the API.
    
    Ensures that a customer can be deleted correctly.
    """
    customer = Customer.objects.create(name="Alice", email="alice@example.com")
    url = f'/api/v1/customers/{customer.id}/'
    response = api_client[0].delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Customer.objects.count() == 0


@pytest.mark.django_db
def test_retrieve_customer(api_client):
    """
    Test retrieving a single customer via the API.
    
    Ensures that a customer's details can be retrieved correctly by their ID.
    """
    customer = Customer.objects.create(name="Alice", email="alice@example.com")
    url = f'/api/v1/customers/{customer.id}/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == "Alice"
    assert response.data['email'] == "alice@example.com"


@pytest.mark.django_db
def test_search_customers(api_client):
    """
    Test searching for customers via the API.
    
    Ensures that customers can be searched by name, email, celular, or address.
    """
    Customer.objects.create(name="Alice", email="alice@example.com")
    Customer.objects.create(name="Bob", email="bob@example.com")
    url = '/api/v1/customers/?search=Alice'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Alice'


@pytest.mark.django_db
def test_filter_customers(api_client):
    """
    Test filtering customers via the API.
    
    Ensures that customers can be filtered by is_active status and city.
    """
    Customer.objects.create(name="Alice", email="alice@example.com", city=Customer.CITY_ARROYO_CABRAL, is_active=True)
    Customer.objects.create(name="Bob", email="bob@example.com", city=Customer.CITY_LUCA, is_active=False)
    
    # Filter by city
    url = '/api/v1/customers/?city=ac'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Alice'
    
    # Filter by active status
    url = '/api/v1/customers/?is_active=true'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Alice'
    
    # Filter by city and active status
    url = '/api/v1/customers/?city=lc&is_active=false'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Bob'