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
        fields = ('id', 'barcode', 'name', 'public_price', 'wholesale_price')


class SaleDetailSerializer(serializers.ModelSerializer):
    """Sale detail serializer."""

    class Meta:
        """Meta options."""

        model = SaleDetail
        fields = ('product', 'quantity', 'unit_price', 'subtotal')
        read_only_fields = ('sale', 'subtotal')


class SaleSerializer(serializers.ModelSerializer):
    """Sale serializer."""

    sale_details = SaleDetailSerializer(many=True, read_only=True)

    class Meta:
        """Meta options."""
        
        model = Sale
        fields = (
            'pk', 'date', 'customer', 'is_bakery', 'payment_method',
            'total', 'total_charged', 'delivered', 'sale_details', 'created', 'modified'
        )
        read_only_fields = ('created', 'modified')

    def create(self, validated_data):
        """Create sale."""
        sale_details_data = validated_data.pop('sale_details', [])
        sale = Sale.objects.create(**validated_data)
        sale.save()

        for detail_data in sale_details_data:
            detail_data['sale'] = sale
            detail_serializer = SaleDetailSerializer(data=detail_data, context={'sale': sale})
            if not detail_serializer.is_valid():
                print("Detail Serializer Errors: ", detail_serializer.errors)
            detail_serializer.save()

        sale.calculate_total()
        return sale

    def update(self, instance, validated_data):
        """Update sale."""
        sale_details_data = validated_data.pop('sale_details', None)

        instance.customer = validated_data.get('customer', instance.customer)
        instance.is_bakery = validated_data.get('is_bakery', instance.is_bakery)
        instance.payment_method = validated_data.get('payment_method', instance.payment_method)
        instance.total = validated_data.get('total', instance.total)
        instance.total_charged = validated_data.get('total_charged', instance.total_charged)
        instance.delivered = validated_data.get('delivered', instance.delivered)

        if sale_details_data:
            instance.sale_details.all().delete()
            for detail_data in sale_details_data:
                detail_data['sale'] = instance
                detail_serializer = SaleDetailSerializer(data=detail_data, context={'sale': instance})
                if not detail_serializer.is_valid():
                    print("Detail Serializer Errors: ", detail_serializer.errors)
                detail_serializer.save()

            instance.calculate_total()

        instance.save()
        return instance
