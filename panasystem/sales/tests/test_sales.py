"""Test sales."""

# Pytest
import pytest

# Django
from django.utils.timezone import now

# Django REST Framework
from rest_framework import status

# Models
from panasystem.sales.models import Sale, SaleDetail
from panasystem.products.models import Product, Category, Brand
from panasystem.customers.models import Customer
from panasystem.suppliers.models import Supplier

# Serializers
from panasystem.sales.serializers import SaleSerializer

# Utilities
from datetime import datetime

# Utils
from panasystem.utils.connect_api_tests import api_client


@pytest.mark.django_db
def test_sale_creation():
    """
    Test creation of a sale model instance.
    
    Ensures that a Sale object is created with the expected attributes.
    """
    customer = Customer.objects.create(name="John Doe")
    sale = Sale.objects.create(
        customer=customer,
        is_bakery=False,
        payment_method=Sale.PAYMENT_METHOD_CASH,
        total=100.0,
        total_charged=100.0,
        delivered=True
    )
    assert sale.customer == customer
    assert sale.is_bakery is False
    assert sale.payment_method == Sale.PAYMENT_METHOD_CASH
    assert sale.total == 100.0
    assert sale.total_charged == 100.0
    assert sale.delivered is True
    assert str(sale) == f'Sale #{sale.pk} - {sale.date} - ${sale.total}'


@pytest.mark.django_db
def test_sale_serializer():
    """
    Test the serialization of a Sale model instance.
    
    Ensures that the SaleSerializer correctly serializes the Sale object.
    """
    customer = Customer.objects.create(name="John Doe")
    sale = Sale.objects.create(
        customer=customer,
        is_bakery=False,
        payment_method=Sale.PAYMENT_METHOD_CASH,
        total=100.0,
        total_charged=100.0,
        delivered=True
    )
    serializer = SaleSerializer(sale)
    data = serializer.data
    assert data['customer'] == customer.id
    assert data['is_bakery'] is False
    assert data['payment_method'] == Sale.PAYMENT_METHOD_CASH
    assert data['total'] == '100.00'
    assert data['total_charged'] == '100.00'
    assert data['delivered'] is True


@pytest.mark.django_db
def test_create_detailed_sale(api_client):
    """
    Test creating a sale with detailed line items via the API.
    
    Ensures that a sale and its details are correctly created.
    """
    customer = Customer.objects.create(name="John Doe")
    category = Category.objects.create(name="Bakery")
    brand = Brand.objects.create(name="BrandX")
    supplier = Supplier.objects.create(name="Supplier Inc.")
    product = Product.objects.create(
        name="Bread",
        category=category,
        public_price=1,
        wholesale_price=1.50,
        brand=brand,
        supplier=supplier,
        current_stock=100
    )
    url = '/api/v1/sales/'
    data = {
        'customer': customer.id,
        'is_bakery': False,
        'payment_method': Sale.PAYMENT_METHOD_CASH,
        'total': 10.0,
        'total_charged': 10.0,
        'delivered': True,
        'sale_details': [
            {
                'product': product.id,
                'quantity': 10,
                'unit_price': product.public_price,
                'subtotal': 10
            }
        ]
    }
    response = api_client[0].post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Sale.objects.count() == 1
    assert SaleDetail.objects.count() == 1
    assert Sale.objects.get().total == 10.0


@pytest.mark.django_db
def test_create_fast_sale(api_client):
    """
    Test creating a fast sale with minimal details via the API.
    
    Ensures that a sale without detailed line items is correctly created.
    """
    category = Category.objects.create(name="Bakery")
    brand = Brand.objects.create(name="BrandX")
    supplier = Supplier.objects.create(name="Supplier Inc.")
    Product.objects.create(
        name="Bread",
        category=category,
        public_price=1,
        wholesale_price=1.50,
        brand=brand,
        supplier=supplier,
        current_stock=100
    )
    url = '/api/v1/sales/'
    data = {
        'total': 5000
    }
    response = api_client[0].post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Sale.objects.count() == 1
    assert SaleDetail.objects.count() == 0
    assert Sale.objects.get().total == 5000


@pytest.mark.django_db
def test_create_multiple_bakery_sales(api_client):
    """
    Test creating multiple bakery sales in a single API request.
    
    Ensures that multiple sales with detailed line items are correctly created.
    """
    
    # Create a customer
    customer = Customer.objects.create(name="John Doe")

    # Create category, brand, and products
    category = Category.objects.create(name="Bakery", description="Bakery products")
    brand = Brand.objects.create(name="BrandX", description="BrandX products")
    product1 = Product.objects.create(
        name="Bread",
        category=category,
        public_price=1.99,
        wholesale_price=1.50,
        brand=brand,
        current_stock=100
    )
    product2 = Product.objects.create(
        name="Milk",
        category=category,
        public_price=0.99,
        wholesale_price=0.75,
        brand=brand,
        current_stock=100
    )

    # Generate sales data
    sales_data = []
    for i in range(10):
        sale_details = [
            {
                'product': product1.id,
                'quantity': 2,
                'unit_price': product1.wholesale_price,
                'subtotal': 2 * product1.wholesale_price
            },
            {
                'product': product2.id,
                'quantity': 3,
                'unit_price': product2.wholesale_price,
                'subtotal': 3 * product2.wholesale_price
            }
        ]
        total = sum(detail['subtotal'] for detail in sale_details)
        sale = {
            'customer': customer.id,
            'is_bakery': True,
            'payment_method': Sale.PAYMENT_METHOD_CASH,
            'total': total,
            'total_charged': total,
            'delivered': False,
            'sale_details': sale_details
        }
        sales_data.append(sale)

    url = '/api/v1/sales/'
    response = api_client[0].post(url, sales_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Sale.objects.count() == 10
    for i, sale in enumerate(Sale.objects.all()):
        assert sale.customer == customer
        assert sale.is_bakery is True
        assert sale.payment_method == Sale.PAYMENT_METHOD_CASH
        assert sale.total_charged == sale.total
        assert sale.delivered == False
        assert sale.sale_details.count() == 2


@pytest.mark.django_db
def test_list_sales(api_client):
    """
    Test listing all sales via the API.
    
    Ensures that the list of sales is retrieved correctly.
    """
    customer = Customer.objects.create(name="John Doe")
    Sale.objects.create(
        customer=customer,
        is_bakery=False,
        payment_method=Sale.PAYMENT_METHOD_CASH,
        total=100.0,
        total_charged=100.0,
        delivered=True
    )
    Sale.objects.create(
        customer=customer,
        is_bakery=False,
        payment_method=Sale.PAYMENT_METHOD_CASH,
        total=50.0,
        total_charged=50.0,
        delivered=True
    )
    url = '/api/v1/sales/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2


@pytest.mark.django_db
def test_list_undelivered_sales(api_client):
    """
    Test listing undelivered sales via the API.
    
    Ensures that only undelivered sales are retrieved when filtered by 'delivered=False'.
    """
    customer = Customer.objects.create(name="John Doe")
    Sale.objects.create(
        customer=customer,
        is_bakery=False,
        payment_method=Sale.PAYMENT_METHOD_CASH,
        total=100.0,
        total_charged=100.0,
        delivered=False
    )
    Sale.objects.create(
        customer=customer,
        is_bakery=False,
        payment_method=Sale.PAYMENT_METHOD_CASH,
        total=50.0,
        total_charged=50.0,
        delivered=True
    )
    url = '/api/v1/sales/?delivered=False'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1


@pytest.mark.django_db
def test_list_not_total_charged_sales(api_client):
    """
    Test listing sales where total_charged is less than total.

    Ensures that only sales where total_charged < total are retrieved.
    """
    customer = Customer.objects.create(name="John Doe")
    Sale.objects.create(
        customer=customer,
        is_bakery=False,
        payment_method=Sale.PAYMENT_METHOD_CASH,
        total=100.0,
        total_charged=50,
        delivered=False
    )
    Sale.objects.create(
        customer=customer,
        is_bakery=False,
        payment_method=Sale.PAYMENT_METHOD_CASH,
        total=50.0,
        total_charged=0,
        delivered=True
    )
    url = '/api/v1/sales/?total_charged_lt_total=True'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    results = response.data['results']
    assert len(response.data['results']) == 2
    assert results[0]['total_charged'] < results[0]['total']


@pytest.mark.django_db
def test_update_sale(api_client):
    """
    Test updating a sale via the API.

    Ensures that a sale can be updated correctly.
    """
    customer = Customer.objects.create(name="John Doe")
    sale = Sale.objects.create(
        customer=customer,
        is_bakery=False,
        payment_method=Sale.PAYMENT_METHOD_CASH,
        total=100.0,
        total_charged=100.0,
        delivered=True
    )
    url = f'/api/v1/sales/{sale.id}/'
    data = {
        'customer': customer.id,
        'is_bakery': True,
        'payment_method': Sale.PAYMENT_METHOD_TRANSFER,
        'total': 150.0,
        'total_charged': 150.0,
        'delivered': False
    }
    response = api_client[0].put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    sale.refresh_from_db()
    assert sale.is_bakery is True
    assert sale.payment_method == Sale.PAYMENT_METHOD_TRANSFER
    assert sale.total == 150.0
    assert sale.total_charged == 150.0
    assert sale.delivered is False


@pytest.mark.django_db
def test_delete_sale(api_client):
    """
    Test deleting a sale via the API.

    Ensures that a sale can be deleted correctly.
    """
    customer = Customer.objects.create(name="John Doe")
    sale = Sale.objects.create(
        customer=customer,
        is_bakery=False,
        payment_method=Sale.PAYMENT_METHOD_CASH,
        total=100.0,
        total_charged=100.0,
        delivered=True
    )
    url = f'/api/v1/sales/{sale.id}/'
    response = api_client[0].delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Sale.objects.count() == 0


@pytest.mark.django_db
def test_retrieve_sale(api_client):
    """
    Test retrieving a single sale via the API.
    
    Ensures that a sale can be retrieved correctly by its ID.
    """
    customer = Customer.objects.create(name="John Doe")
    sale = Sale.objects.create(
        customer=customer,
        is_bakery=False,
        payment_method=Sale.PAYMENT_METHOD_CASH,
        total=100.0,
        total_charged=100.0,
        delivered=True
    )
    url = f'/api/v1/sales/{sale.id}/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['customer'] == customer.id
    assert response.data['is_bakery'] is False
    assert response.data['payment_method'] == Sale.PAYMENT_METHOD_CASH
    assert response.data['total'] == '100.00'
    assert response.data['total_charged'] == '100.00'
    assert response.data['delivered'] is True


@pytest.mark.django_db
def test_get_sale_totals(api_client):
    """
    Test retrieving total sales and sum of totals via the API.

    Ensures that the total number of sales and their sum can be retrieved correctly.
    """
    customer = Customer.objects.create(name="John Doe")
    Sale.objects.create(
        customer=customer,
        is_bakery=False,
        payment_method=Sale.PAYMENT_METHOD_CASH,
        total=100.0,
        total_charged=100.0,
        delivered=True,
        date=datetime(2024, 1, 1)
    )
    Sale.objects.create(
        customer=customer,
        is_bakery=False,
        payment_method=Sale.PAYMENT_METHOD_TRANSFER,
        total=150.0,
        total_charged=150.0,
        delivered=True,
        date=datetime(2024, 1, 2)
    )
    url = '/api/v1/sales/totals/?date_from=2024-01-01&date_to=2024-12-31'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['total_sales'] == 2
    assert response.data['sum_total'] == 250.0