"""Suppliers views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter

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
    """Suppliers viewset.
    
    Functions:
        - Create a supplier
        - List suppliers:
            * Search by 'name, celular'.
        - Retrieve a supplier.
        - Update a supplier.
        - Delete a supplier.
    """

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'celular')
    