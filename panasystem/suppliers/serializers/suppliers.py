"""Suppliers serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from panasystem.suppliers.models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    """Supplier serializer."""

    class Meta:
        """Meta options."""

        model = Supplier
        fields = '__all__'