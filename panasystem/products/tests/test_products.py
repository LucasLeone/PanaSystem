"""Test products."""

# Pytest
import pytest

# Django REST Framework
from rest_framework import status

# Models
from panasystem.products.models import Product, Category, Brand
from panasystem.suppliers.models import Supplier

# Serializers
from panasystem.products.serializers import ProductSerializer

# Utils
from panasystem.utils.connect_api_tests import api_client


@pytest.mark.django_db
def test_product_creation():
    """
    Test the creation of a Product model instance.
    
    Ensures that a Product object is created with the expected attributes.
    """
    category = Category.objects.create(name="Bakery", description="Bakery products")
    brand = Brand.objects.create(name="BrandX", description="BrandX products")
    supplier = Supplier.objects.create(name="Supplier Inc.")
    product = Product.objects.create(
        name="Bread",
        category=category,
        public_price=1.99,
        wholesale_price=1.50,
        brand=brand,
        supplier=supplier,
        current_stock=100
    )
    assert product.name == "Bread"
    assert product.category == category
    assert product.public_price == 1.99
    assert product.wholesale_price == 1.50
    assert product.brand == brand
    assert product.supplier == supplier
    assert product.current_stock == 100
    assert str(product) == "Bread"


@pytest.mark.django_db
def test_product_serializer():
    """
    Test the serialization of a Product model instance.
    
    Ensures that the ProductSerializer correctly serializes the Product object.
    """
    category = Category.objects.create(name="Bakery", description="Bakery products")
    brand = Brand.objects.create(name="BrandX", description="BrandX products")
    supplier = Supplier.objects.create(name="Supplier Inc.")
    product = Product(
        name="Bread",
        category=category,
        public_price=1.99,
        wholesale_price=1.50,
        brand=brand,
        supplier=supplier,
        current_stock=100
    )
    product.save()  # Ensure the product has a pk before serialization
    serializer = ProductSerializer(product)
    data = serializer.data
    assert data['name'] == "Bread"
    assert data['category'] == category.id
    assert data['public_price'] == "1.99"
    assert data['wholesale_price'] == "1.50"
    assert data['brand'] == brand.id
    assert data['supplier'] == supplier.id


@pytest.mark.django_db
def test_create_product(api_client):
    """
    Test creating a product via the API.
    
    Ensures that a product is correctly created and saved to the database.
    """
    category = Category.objects.create(name="Bakery", description="Bakery products")
    brand = Brand.objects.create(name="BrandX", description="BrandX products")
    supplier = Supplier.objects.create(name="Supplier Inc.")
    url = '/api/v1/products/'
    data = {
        'name': 'Bread',
        'category': category.id,
        'public_price': 1.99,
        'wholesale_price': 1.50,
        'brand': brand.id,
        'supplier': supplier.id,
        'current_stock': 100
    }
    response = api_client[0].post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Product.objects.count() == 1
    assert Product.objects.get().name == 'Bread'


@pytest.mark.django_db
def test_list_products(api_client):
    """
    Test listing all products via the API.
    
    Ensures that the list of products is retrieved correctly.
    """
    category = Category.objects.create(name="Bakery", description="Bakery products")
    brand = Brand.objects.create(name="BrandX", description="BrandX products")
    supplier = Supplier.objects.create(name="Supplier Inc.")
    Product.objects.create(name="Bread", category=category, public_price=1.99, brand=brand, supplier=supplier)
    Product.objects.create(name="Milk", category=category, public_price=0.99, brand=brand, supplier=supplier)
    url = '/api/v1/products/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_update_product(api_client):
    """
    Test updating a product via the API.
    
    Ensures that a product's details can be updated correctly.
    """
    category = Category.objects.create(name="Bakery", description="Bakery products")
    brand = Brand.objects.create(name="BrandX", description="BrandX products")
    supplier = Supplier.objects.create(name="Supplier Inc.")
    product = Product.objects.create(name="Bread", category=category, public_price=1.99, brand=brand, supplier=supplier)
    url = f'/api/v1/products/{product.id}/'
    data = {
        'name': 'Bread Updated',
        'category': category.id,
        'public_price': 2.50,
        'wholesale_price': 2.00,
        'brand': brand.id,
        'supplier': supplier.id,
        'current_stock': 150
    }
    response = api_client[0].put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    product.refresh_from_db()
    assert product.name == 'Bread Updated'
    assert product.public_price == 2.50
    assert product.wholesale_price == 2.00
    assert product.current_stock == 150


@pytest.mark.django_db
def test_delete_product(api_client):
    """
    Test deleting a product via the API.
    
    Ensures that a product can be deleted correctly.
    """
    category = Category.objects.create(name="Bakery", description="Bakery products")
    brand = Brand.objects.create(name="BrandX", description="BrandX products")
    supplier = Supplier.objects.create(name="Supplier Inc.")
    product = Product.objects.create(name="Bread", category=category, public_price=1.99, brand=brand, supplier=supplier)
    url = f'/api/v1/products/{product.id}/'
    response = api_client[0].delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Product.objects.count() == 0


@pytest.mark.django_db
def test_retrieve_product(api_client):
    """
    Test retrieving a single product via the API.
    
    Ensures that a product's details can be retrieved correctly by its ID.
    """
    category = Category.objects.create(name="Bakery", description="Bakery products")
    brand = Brand.objects.create(name="BrandX", description="BrandX products")
    supplier = Supplier.objects.create(name="Supplier Inc.")
    product = Product.objects.create(name="Bread", category=category, public_price=1.99, wholesale_price=1.50, brand=brand, supplier=supplier)
    url = f'/api/v1/products/{product.id}/'
    response = api_client[0].get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == "Bread"
    assert response.data['category'] == category.id
    assert response.data['public_price'] == "1.99"
    assert response.data['wholesale_price'] == "1.50"
    assert response.data['brand'] == brand.id
    assert response.data['supplier'] == supplier.id