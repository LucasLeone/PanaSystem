"""Orders views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Serializers
from panasystem.suppliers.serializers import OrderSerializer

# Models
from panasystem.suppliers.models import Order
from panasystem.products.models import Product


class OrderViewSet(mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    """Order viewset.
    
    Functions:
        - Create an order.
        - List orders:
            * Filter by 'supplier'.
            * Search by 'description'.
        - Retrieve an order.
        - Update an order.
        - Delete an order.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('supplier',)
    search_fields = ('description',)
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
