"""Suppliers views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

# Serializers
from panasystem.suppliers.serializers import SupplierSerializer

# Models
from panasystem.suppliers.models import Supplier


class SuppliersViewSet(mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    """
    ViewSet for managing suppliers.

    Provides the following actions:
    - Create a supplier
    - List suppliers with optional search by 'name' and 'celular'
    - Retrieve a specific supplier
    - Update a supplier's details
    - Delete a supplier

    Permissions:
    - Requires the user to be authenticated to perform any action.
    """

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'celular')
    permission_classes = [IsAuthenticated]
    pagination_class = None