"""Customers serializers."""

# Django REST Framework
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

# Models
from panasystem.customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Customer serializer."""

    city_display = serializers.SerializerMethodField()

    class Meta:
        """Meta options."""
        model = Customer
        fields = (
            'pk',
            'name',
            'celular',
            'email',
            'address',
            'city',
            'city_display',
            'is_active'
        )
        extra_kwargs = {
            'city': {'write_only': True}
        }

    @extend_schema_field(serializers.CharField)
    def get_city_display(self, obj):
        return obj.get_city_display()
