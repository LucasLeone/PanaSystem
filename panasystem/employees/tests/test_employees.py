"""Test employees."""

# Pytest
import pytest

# Django REST Framework
from rest_framework import status

# Models
from panasystem.employees.models import Employee

# Serializers
from panasystem.employees.serializers import EmployeeSerializer

# Utils
from panasystem.utils.connect_api_tests import api_client


@pytest.mark.django_db
def test_employee_creation():
    """
    Test the creation of an Employee model instance.
    
    Ensures that an Employee object is created with the expected attributes.
    """
    employee = Employee.objects.create(name="John Doe")
    assert employee.name == "John Doe"
    assert str(employee) == "John Doe"


def test_employee_serializer():
    """
    Test the serialization of an Employee model instance.
    
    Ensures that the EmployeeSerializer correctly serializes the Employee object.
    """
    employee = Employee(name="Jane Doe")
    serializer = EmployeeSerializer(employee)
    data = serializer.data
    assert data['name'] == "Jane Doe"


@pytest.mark.django_db
def test_create_employee(api_client):
    """
    Test creating an employee via the API.
    
    Ensures that an employee is correctly created and saved to the database.
    """
    url = '/api/v1/employees/'
    data = {'name': 'John Doe'}
    response = api_client[0].post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Employee.objects.count() == 1
    assert Employee.objects.get().name == 'John Doe'


@pytest.mark.django_db
def test_list_employees(api_client):
    """
    Test listing all employees via the API.
    
    Ensures that the list of employees is retrieved correctly.
    """
    Employee.objects.create(name="John Doe")
    Employee.objects.create(name="Jane Doe")
    url = '/api/v1/employees/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_update_employee(api_client):
    """
    Test updating an employee via the API.
    
    Ensures that an employee's details can be updated correctly.
    """
    employee = Employee.objects.create(name="John Doe")
    url = f'/api/v1/employees/{employee.id}/'
    data = {'name': 'John Smith'}
    response = api_client[0].put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    employee.refresh_from_db()
    assert employee.name == 'John Smith'


@pytest.mark.django_db
def test_delete_employee(api_client):
    """
    Test deleting an employee via the API.
    
    Ensures that an employee can be deleted correctly.
    """
    employee = Employee.objects.create(name="John Doe")
    url = f'/api/v1/employees/{employee.id}/'
    response = api_client[0].delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Employee.objects.count() == 0


@pytest.mark.django_db
def test_retrieve_employee(api_client):
    """
    Test retrieving a single employee via the API.
    
    Ensures that an employee's details can be retrieved correctly by their ID.
    """
    employee = Employee.objects.create(name="John Doe")
    url = f'/api/v1/employees/{employee.id}/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == "John Doe"


@pytest.mark.django_db
def test_search_employees(api_client):
    """
    Test searching for employees via the API.
    
    Ensures that employees can be searched by name.
    """
    Employee.objects.create(name="John Doe")
    Employee.objects.create(name="Jane Doe")
    url = '/api/v1/employees/?search=John'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'John Doe'