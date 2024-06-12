"""Test expenses."""

# Pytest
import pytest

# Django
from panasystem.users.models import User

# Django REST Framework
from rest_framework.test import APIClient
from rest_framework import status

# Models
from panasystem.expenses.models import Expense, ExpenseCategory
from panasystem.employees.models import Employee
from panasystem.suppliers.models import Supplier

# Serializers
from panasystem.expenses.serializers import ExpenseSerializer

# Utils
from panasystem.utils.connect_api_tests import api_client


@pytest.mark.django_db
def test_expense_creation():
    """
    Test the creation of an Expense model instance.
    
    Ensures that an Expense object is created with the expected attributes.
    """
    category = ExpenseCategory.objects.create(name="Utilities", description="Monthly utility bills")
    employee = Employee.objects.create(name="John Doe")
    expense = Expense.objects.create(
        total=100,
        description="Electricity bill",
        category=category,
        employee=employee
    )
    assert expense.total == 100
    assert expense.description == "Electricity bill"
    assert str(expense) == f"Expense #{expense.pk}: $100"


def test_expense_serializer():
    """
    Test the serialization of an Expense model instance.
    
    Ensures that the ExpenseSerializer correctly serializes the Expense object.
    """
    category = ExpenseCategory(name="Utilities", description="Monthly utility bills")
    employee = Employee(name="John Doe")
    supplier = Supplier(name="Supplier Inc.")
    expense = Expense(
        total=100,
        description="Electricity bill",
        category=category,
        employee=employee,
        supplier=supplier
    )
    serializer = ExpenseSerializer(expense)
    data = serializer.data
    assert data['total'] == 100
    assert data['description'] == "Electricity bill"
    assert data['category'] == category.id
    assert data['employee'] == employee.id
    assert data['supplier'] == supplier.id


@pytest.mark.django_db
def test_create_expense(api_client):
    """
    Test creating an expense via the API.
    
    Ensures that an expense is correctly created and saved to the database.
    """
    category = ExpenseCategory.objects.create(name="Utilities", description="Monthly utility bills")
    employee = Employee.objects.create(name="John Doe")
    url = '/api/v1/expenses/'
    data = {
        'total': 100,
        'description': 'Electricity bill',
        'category': category.id,
        'employee': employee.id
    }
    response = api_client[0].post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Expense.objects.count() == 1
    assert Expense.objects.get().description == 'Electricity bill'


@pytest.mark.django_db
def test_list_expenses(api_client):
    """
    Test listing all expenses via the API.
    
    Ensures that the list of expenses is retrieved correctly.
    """
    category = ExpenseCategory.objects.create(name="Utilities", description="Monthly utility bills")
    employee = Employee.objects.create(name="John Doe")
    Expense.objects.create(total=100, description="Electricity bill", category=category, employee=employee)
    Expense.objects.create(total=200, description="Water bill", category=category, employee=employee)
    url = '/api/v1/expenses/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_update_expense(api_client):
    """
    Test updating an expense via the API.
    
    Ensures that an expense's details can be updated correctly.
    """
    category = ExpenseCategory.objects.create(name="Utilities", description="Monthly utility bills")
    employee = Employee.objects.create(name="John Doe")
    expense = Expense.objects.create(total=100, description="Electricity bill", category=category, employee=employee)
    url = f'/api/v1/expenses/{expense.id}/'
    data = {'total': 150, 'description': 'Electricity and Water bill', 'category': category.id, 'employee': employee.id}
    response = api_client[0].put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    expense.refresh_from_db()
    assert expense.total == 150
    assert expense.description == 'Electricity and Water bill'


@pytest.mark.django_db
def test_delete_expense(api_client):
    """
    Test deleting an expense via the API.
    
    Ensures that an expense can be deleted correctly.
    """
    category = ExpenseCategory.objects.create(name="Utilities", description="Monthly utility bills")
    employee = Employee.objects.create(name="John Doe")
    expense = Expense.objects.create(total=100, description="Electricity bill", category=category, employee=employee)
    url = f'/api/v1/expenses/{expense.id}/'
    response = api_client[0].delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Expense.objects.count() == 0


@pytest.mark.django_db
def test_retrieve_expense(api_client):
    """
    Test retrieving a single expense via the API.
    
    Ensures that an expense's details can be retrieved correctly by its ID.
    """
    category = ExpenseCategory.objects.create(name="Utilities", description="Monthly utility bills")
    employee = Employee.objects.create(name="John Doe")
    expense = Expense.objects.create(total=100, description="Electricity bill", category=category, employee=employee)
    url = f'/api/v1/expenses/{expense.id}/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['description'] == "Electricity bill"
    assert response.data['total'] == 100


@pytest.mark.django_db
def test_search_expenses(api_client):
    """
    Test searching expenses by description via the API.
    
    Ensures that expenses can be searched by their description field.
    """
    category = ExpenseCategory.objects.create(name="Utilities", description="Monthly utility bills")
    employee = Employee.objects.create(name="John Doe")
    Expense.objects.create(total=100, description="Electricity bill", category=category, employee=employee)
    Expense.objects.create(total=200, description="Water bill", category=category, employee=employee)
    url = '/api/v1/expenses/?search=Electricity'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['description'] == 'Electricity bill'


@pytest.mark.django_db
def test_filter_expenses(api_client):
    """
    Test filtering expenses by employee, category, supplier, and date via the API.
    
    Ensures that expenses can be filtered correctly based on different fields.
    """
    category = ExpenseCategory.objects.create(name="Utilities", description="Monthly utility bills")
    employee = Employee.objects.create(name="John Doe")
    supplier = Supplier.objects.create(name="Supplier Inc.")
    
    Expense.objects.create(total=100, description="Electricity bill", category=category, employee=employee, supplier=supplier)
    Expense.objects.create(total=200, description="Water bill", category=category, employee=employee, supplier=supplier)
    
    # Filter by employee
    url = f'/api/v1/expenses/?employee={employee.id}'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    
    # Filter by category
    url = f'/api/v1/expenses/?category={category.id}'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    
    # Filter by supplier
    url = f'/api/v1/expenses/?supplier={supplier.id}'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    
    # Filter by date
    expense_date = Expense.objects.first().date
    url = f'/api/v1/expenses/?date={expense_date.date()}'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2