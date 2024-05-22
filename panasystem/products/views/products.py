"""Products views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

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
    """Product view set.
    
    Functions:
        - Create a product.
        - List products:
            * Filter by 'category, brand, supplier'.
            * Order by 'code, name'.
        - Retrieve a product.
        - Update a product.
        - Delete a product.
    """
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('category', 'brand', 'supplier')
    search_fields = ('code', 'name')
    ordering_fields = ('code', 'name')
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class CategoryViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Category view set.
    
    Functions:
        - Create a category.
        - List categories:
            * Search by 'name'.
        - Retrieve a category.
        - Update a category.
        - Delete a category.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class BrandViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Brand view set.
    
    Functions:
        - Create a brand.
        - List brands:
            * Search by 'name'.
        - Retrieve a brand.
        - Update a brand.
        - Delete a brand.
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]