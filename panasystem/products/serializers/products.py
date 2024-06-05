"""Products serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from panasystem.products.models import Category, Product, PriceHistory, Brand
from panasystem.suppliers.models import Supplier


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""

    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for the Brand model."""

    class Meta:
        model = Brand
        fields = '__all__'


class PriceHistorySerializer(serializers.ModelSerializer):
    """Serializer for the PriceHistory model."""

    class Meta:
        model = PriceHistory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model."""

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), required=False)
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), required=False)
    price_history = PriceHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        """Create product."""

        product = Product.objects.create(**validated_data)
        public_price = validated_data.get('public_price', )
        wholesale_price = validated_data.get('wholesale_price', None)
        if wholesale_price is not None:
            product.update_price(public_price, wholesale_price)
        else:
            product.update_price(public_price, None)

        return product

    def update(self, instance, validated_data):
        """Update product."""

        instance.category = validated_data.get('category', instance.category)
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        public_price = validated_data.get('public_price', instance.public_price)
        wholesale_price = validated_data.get('wholesale_price', instance.wholesale_price)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.description = validated_data.get('description', instance.description)
        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.current_stock = validated_data.get('current_stock', instance.current_stock)

        if public_price != instance.public_price or (wholesale_price is not None and wholesale_price != instance.wholesale_price):
            instance.update_price(public_price, wholesale_price)

        instance.public_price = public_price
        instance.wholesale_price = wholesale_price

        instance.save()
        return instance

