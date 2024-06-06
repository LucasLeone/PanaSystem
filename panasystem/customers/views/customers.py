"""Customer views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

# Serializers
from panasystem.customers.serializers import CustomerSerializer

# Models
from panasystem.customers.models import Customer


class CustomerViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Customer view set.

    Functions:
        - Create a customer.
        - List customer:
            * Filter by 'is_active, city'.
            * Search by 'name, email, celular, address'
        - Retrieve a customer.
        - Delete a customer.
        - Update a customer.
    """
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('is_active', 'city')
    search_fields = ('name', 'email', 'celular', 'address')
    # permission_classes = [IsAuthenticated] HABILITAR EN PRODUCCION
    pagination_class = None