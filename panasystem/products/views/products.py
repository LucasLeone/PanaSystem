"""Products views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Serializers
from panasystem.products.serializers import ProductSerializer, PriceHistorySerializer, CategorySerializer

# Models
from panasystem.products.models import Product, PriceHistory, Category


class ProductViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Product view set."""
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
