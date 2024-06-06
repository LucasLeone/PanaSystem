"""Products serializers."""

# Django REST Framework
from rest_framework import serializers
from django.core.exceptions import ValidationError

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

    category = CategorySerializer()
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), required=False)
    brand = BrandSerializer(required=False)
    price_history = PriceHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'pk',
            'barcode',
            'name',
            'category',
            'public_price',
            'wholesale_price',
            'current_stock',
            'brand',
            'supplier',
            'price_history',
            'description',
            'created',
            'modified'
        )

    def validate_category(self, value):
        """Ensure category exists."""
        if 'name' not in value:
            raise ValidationError("Category name is required")
        category_name = value['name']
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            raise ValidationError(f"Category with name {category_name} does not exist")
        return category

    def validate_brand(self, value):
        """Ensure brand exists if provided."""
        if value and 'name' in value:
            brand_name = value['name']
            try:
                brand = Brand.objects.get(name=brand_name)
            except Brand.DoesNotExist:
                raise ValidationError(f"Brand with name {brand_name} does not exist")
            return brand
        return value

    def create(self, validated_data):
        """Create product."""
        category_data = validated_data.pop('category')
        brand_data = validated_data.pop('brand', None)

        category = self.validate_category(category_data)
        brand = self.validate_brand(brand_data) if brand_data else None

        product = Product.objects.create(category=category, brand=brand, **validated_data)
        public_price = validated_data.get('public_price')
        wholesale_price = validated_data.get('wholesale_price', None)

        if wholesale_price is not None:
            product.update_price(public_price, wholesale_price)
        else:
            product.update_price(public_price, None)

        return product

    def update(self, instance, validated_data):
        """Update product."""
        category_data = validated_data.pop('category', None)
        brand_data = validated_data.pop('brand', None)

        if category_data:
            instance.category = self.validate_category(category_data)

        if brand_data:
            instance.brand = self.validate_brand(brand_data)

        instance.barcode = validated_data.get('barcode', instance.barcode)
        instance.name = validated_data.get('name', instance.name)
        public_price = validated_data.get('public_price', instance.public_price)
        wholesale_price = validated_data.get('wholesale_price', instance.wholesale_price)
        instance.description = validated_data.get('description', instance.description)
        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.current_stock = validated_data.get('current_stock', instance.current_stock)

        if public_price != instance.public_price or (wholesale_price is not None and wholesale_price != instance.wholesale_price):
            instance.update_price(public_price, wholesale_price)

        instance.public_price = public_price
        instance.wholesale_price = wholesale_price

        instance.save()
        return instance
