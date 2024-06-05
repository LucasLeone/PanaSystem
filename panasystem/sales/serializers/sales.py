"""Sales serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from panasystem.sales.models import Sale, SaleDetail
from panasystem.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Product serializer."""

    class Meta:
        """Meta options."""

        model = Product
        fields = ('id', 'code', 'name', 'public_price', 'wholesale_price')


class SaleDetailSerializer(serializers.ModelSerializer):
    """Sale detail serializer."""

    product_info = ProductSerializer(source='product', read_only=True)

    class Meta:
        """Meta options."""
        
        model = SaleDetail
        fields = ('product', 'product_info', 'quantity', 'unit_price', 'subtotal')
        read_only_fields = ('sale', 'subtotal')


class SaleSerializer(serializers.ModelSerializer):
    """Sale serializer."""

    customer_name = serializers.SerializerMethodField()
    
    def get_customer_name(self, obj):
        return obj.customer.name if obj.customer else ''

    sale_details = SaleDetailSerializer(many=True, read_only=True)
    total_help = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        """Meta options."""
        
        model = Sale
        fields = '__all__'
        read_only_fields = ('total_help',)