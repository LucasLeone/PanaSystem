"""Test expense categories."""

# Pytest
import pytest

# Django REST Framework
from rest_framework import status

# Models
from panasystem.expenses.models import ExpenseCategory

# Serializers
from panasystem.expenses.serializers import ExpenseCategorySerializer

# Utils
from panasystem.utils.connect_api_tests import api_client


@pytest.mark.django_db
def test_expense_category_creation():
    """
    Test the creation of an ExpenseCategory model instance.
    
    Ensures that an ExpenseCategory object is created with the expected attributes.
    """
    category = ExpenseCategory.objects.create(name="Utilities", description="Monthly utility bills")
    assert category.name == "Utilities"
    assert category.description == "Monthly utility bills"
    assert str(category) == "Utilities"


def test_expense_category_serializer():
    """
    Test the serialization of an ExpenseCategory model instance.
    
    Ensures that the ExpenseCategorySerializer correctly serializes the ExpenseCategory object.
    """
    category = ExpenseCategory(name="Utilities", description="Monthly utility bills")
    serializer = ExpenseCategorySerializer(category)
    data = serializer.data
    assert data['name'] == "Utilities"
    assert data['description'] == "Monthly utility bills"


@pytest.mark.django_db
def test_create_expense_category(api_client):
    """
    Test creating an expense category via the API.
    
    Ensures that an expense category is correctly created and saved to the database.
    """
    url = '/api/v1/expense-categories/'
    data = {'name': 'Utilities', 'description': 'Monthly utility bills'}
    response = api_client[0].post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert ExpenseCategory.objects.count() == 1
    assert ExpenseCategory.objects.get().name == 'Utilities'


@pytest.mark.django_db
def test_list_expense_categories(api_client):
    """
    Test listing all expense categories via the API.
    
    Ensures that the list of expense categories is retrieved correctly.
    """
    ExpenseCategory.objects.create(name="Utilities", description="Monthly utility bills")
    ExpenseCategory.objects.create(name="Rent", description="Monthly rent payment")
    url = '/api/v1/expense-categories/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_update_expense_category(api_client):
    """
    Test updating an expense category via the API.
    
    Ensures that an expense category's details can be updated correctly.
    """
    category = ExpenseCategory.objects.create(name="Utilities", description="Monthly utility bills")
    url = f'/api/v1/expense-categories/{category.id}/'
    data = {'name': 'Utilities and Rent', 'description': 'Utility bills and rent payment'}
    response = api_client[0].put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    category.refresh_from_db()
    assert category.name == 'Utilities and Rent'
    assert category.description == 'Utility bills and rent payment'


@pytest.mark.django_db
def test_delete_expense_category(api_client):
    """
    Test deleting an expense category via the API.
    
    Ensures that an expense category can be deleted correctly.
    """
    category = ExpenseCategory.objects.create(name="Utilities", description="Monthly utility bills")
    url = f'/api/v1/expense-categories/{category.id}/'
    response = api_client[0].delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert ExpenseCategory.objects.count() == 0


@pytest.mark.django_db
def test_retrieve_expense_category(api_client):
    """
    Test retrieving a single expense category via the API.
    
    Ensures that an expense category's details can be retrieved correctly by its ID.
    """
    category = ExpenseCategory.objects.create(name="Utilities", description="Monthly utility bills")
    url = f'/api/v1/expense-categories/{category.id}/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == "Utilities"
    assert response.data['description'] == "Monthly utility bills"