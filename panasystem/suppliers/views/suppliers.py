"""Suppliers views."""

# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

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
    """Suppliers viewset."""

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer