"""Customers serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from panasystem.customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Customer serializer."""

    class Meta:
        """Meta options."""

        model = Customer
        fields = '__all__'