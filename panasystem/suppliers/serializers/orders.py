"""Orders serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from panasystem.suppliers.models import Order, Supplier


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer."""

    supplier = serializers.SlugRelatedField(slug_field='name', queryset=Supplier.objects.all())

    def get_supplier_name(self, obj):
        """Get supplier name."""
        return obj.supplier.name if obj.supplier else None

    class Meta:
        """Meta options."""

        model = Order
        fields = '__all__'


"""
class OrderDetailSerializer(serializers.ModelSerializer):
    ""Order detail serializer.""

    class Meta:
        ""Meta options.""

        model = OrderDetail
        fields = ['product', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['order', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    ""Order serializer.""

    details = OrderDetailSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        ""Meta options.""
        model = Order
        fields = '__all__'
        read_only_fields = ['total']
"""