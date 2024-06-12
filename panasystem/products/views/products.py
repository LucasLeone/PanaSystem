"""Products views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

# Serializers
from panasystem.products.serializers import ProductSerializer, CategorySerializer, BrandSerializer

# Models
from panasystem.products.models import Product, Category, Brand


class ProductViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    ViewSet for managing products.

    Provides the following actions:
    - Create a product
    - List products with filters by 'category', 'brand', 'supplier', ordering by 'name', and search capability by 'name' and 'barcode'
    - Retrieve a specific product
    - Update a product's details
    - Delete a product

    Permissions:
    - Requires the user to be authenticated to perform any action.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('category', 'brand', 'supplier')
    search_fields = ('barcode', 'name')
    ordering_fields = ('name',)
    permission_classes = [IsAuthenticated]
    pagination_class = None


class ProductCategoryViewSet(mixins.CreateModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.ListModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    """
    ViewSet for managing product categories.

    Provides the following actions:
    - Create a category
    - List categories with search capability by 'name'
    - Retrieve a specific category
    - Update a category's details
    - Delete a category

    Permissions:
    - Requires the user to be authenticated to perform any action.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAuthenticated]
    pagination_class = None


class ProductBrandViewSet(mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """
    ViewSet for managing product brands.

    Provides the following actions:
    - Create a brand
    - List brands with search capability by 'name'
    - Retrieve a specific brand
    - Update a brand's details
    - Delete a brand

    Permissions:
    - Requires the user to be authenticated to perform any action.
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAuthenticated]
    pagination_class = None