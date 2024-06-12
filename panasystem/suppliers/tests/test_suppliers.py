"""Test suppliers."""

# Pytest
import pytest

# Django REST Framework
from rest_framework import status

# Models
from panasystem.suppliers.models import Supplier

# Serializers
from panasystem.suppliers.serializers import SupplierSerializer

# Import the fixture from connect_api_tests
from panasystem.utils.connect_api_tests import api_client


@pytest.mark.django_db
def test_supplier_creation():
    """
    Test the creation of a Supplier model instance.

    Ensures that a Supplier object is created with the expected attributes.
    """
    supplier = Supplier.objects.create(name="Supplier Inc.", celular="123456789")
    assert supplier.name == "Supplier Inc."
    assert supplier.celular == "123456789"
    assert str(supplier) == "Supplier Inc."


@pytest.mark.django_db
def test_supplier_serializer():
    """
    Test the serialization of a Supplier model instance.

    Ensures that the SupplierSerializer correctly serializes the Supplier object.
    """
    supplier = Supplier(name="Supplier Inc.", celular="123456789")
    supplier.save()  # Ensure the supplier has a pk before serialization
    serializer = SupplierSerializer(supplier)
    data = serializer.data
    assert data['name'] == "Supplier Inc."
    assert data['celular'] == "123456789"


@pytest.mark.django_db
def test_create_supplier(api_client):
    """
    Test creating a supplier via the API.

    Ensures that a supplier is correctly created and saved to the database.
    """
    url = '/api/v1/suppliers/'
    data = {
        'name': 'Supplier Inc.',
        'celular': '123456789'
    }
    response = api_client[0].post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Supplier.objects.count() == 1
    assert Supplier.objects.get().name == 'Supplier Inc.'


@pytest.mark.django_db
def test_list_suppliers(api_client):
    """
    Test listing all suppliers via the API.

    Ensures that the list of suppliers is retrieved correctly.
    """
    Supplier.objects.create(name="Supplier Inc.", celular="123456789")
    Supplier.objects.create(name="Another Supplier", celular="987654321")
    url = '/api/v1/suppliers/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_update_supplier(api_client):
    """
    Test updating a supplier via the API.

    Ensures that a supplier's details can be updated correctly.
    """
    supplier = Supplier.objects.create(name="Supplier Inc.", celular="123456789")
    url = f'/api/v1/suppliers/{supplier.id}/'
    data = {
        'name': 'Supplier Inc. Updated',
        'celular': '987654321'
    }
    response = api_client[0].put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    supplier.refresh_from_db()
    assert supplier.name == 'Supplier Inc. Updated'
    assert supplier.celular == '987654321'


@pytest.mark.django_db
def test_delete_supplier(api_client):
    """
    Test deleting a supplier via the API.

    Ensures that a supplier can be deleted correctly.
    """
    supplier = Supplier.objects.create(name="Supplier Inc.", celular="123456789")
    url = f'/api/v1/suppliers/{supplier.id}/'
    response = api_client[0].delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Supplier.objects.count() == 0


@pytest.mark.django_db
def test_retrieve_supplier(api_client):
    """
    Test retrieving a single supplier via the API.

    Ensures that a supplier's details can be retrieved correctly by its ID.
    """
    supplier = Supplier.objects.create(name="Supplier Inc.", celular="123456789")
    url = f'/api/v1/suppliers/{supplier.id}/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == "Supplier Inc."
    assert response.data['celular'] == "123456789"