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
    """
    ViewSet for managing customers.

    Provides the following actions:
    - Create a customer
    - List customers with filtering and search capabilities
        * Filter by 'is_active' and 'city'
        * Search by 'name', 'email', 'celular', and 'address'
    - Retrieve a specific customer
    - Update a customer's details
    - Delete a customer

    Permissions:
    - Requires the user to be authenticated to perform any action.
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('is_active', 'city')
    search_fields = ('name', 'email', 'celular', 'address')
    permission_classes = [IsAuthenticated]
    pagination_class = None