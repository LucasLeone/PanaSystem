"""Sales serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from panasystem.sales.models import Sale, SaleDetail


class SaleDetailSerializer(serializers.ModelSerializer):
    """Sale detail serializer."""

    class Meta:
        """Meta option."""
        
        model = SaleDetail
        fields = ('product', 'quantity', 'unit_price', 'subtotal')
        read_only_fields = ('sale', 'subtotal')


class SaleSerializer(serializers.ModelSerializer):
    """Sale serializer."""

    sale_details = SaleDetailSerializer(many=True, read_only=True)
    total_help = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        """Meta option."""
        
        model = Sale
        fields = '__all__'
        read_only_fields = ('total_help',)
        