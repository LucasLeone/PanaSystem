"""Products serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from panasystem.products.models import Category, Product, PriceHistory
from panasystem.suppliers.models import Supplier

# Serializers
from panasystem.suppliers.serializers import SupplierSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""

    class Meta:
        model = Category
        fields = '__all__'


class PriceHistorySerializer(serializers.ModelSerializer):
    """Serializer for the PriceHistory model."""

    class Meta:
        model = PriceHistory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model."""

    category = CategorySerializer()
    supplier = SupplierSerializer()

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        """Create product."""

        category_data = validated_data.pop('category')
        supplier_data = validated_data.pop('supplier')
        category = Category.objects.get_or_create(**category_data)[0]
        supplier, created = Supplier.objects.get_or_create(**supplier_data)
        product = Product.objects.create(category=category, supplier=supplier, **validated_data)
        public_price = validated_data.get('public_price', None)
        wholesale_price = validated_data.get('wholesale_price', None)
        if wholesale_price is not None:
            product.update_price(public_price, wholesale_price)
        else:
            product.update_price(public_price, None)

        return product

    def update(self, instance, validated_data):
        """Update product."""

        category_data = validated_data.pop('category')
        category_instance, created = Category.objects.get_or_create(**category_data)
        instance.category = category_instance
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        public_price = validated_data.get('public_price', instance.public_price)
        wholesale_price = validated_data.get('wholesale_price', None)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.description = validated_data.get('description', instance.description)
        supplier_data = validated_data.get('supplier')
        if supplier_data:
            supplier_instance, created = Supplier.objects.get_or_create(**supplier_data)
            instance.supplier = supplier_instance

        if public_price != instance.public_price:
            print(wholesale_price)
            if wholesale_price is not None:
                if wholesale_price != instance.wholesale_price:
                    instance.update_price(public_price, wholesale_price)
                else:
                    instance.update_price(public_price, instance.wholesale_price)
            else:
                instance.update_price(public_price, None)
        elif public_price == instance.public_price and wholesale_price != instance.public_price:
            instance.update_price(instance.public_price, wholesale_price)

        instance.public_price = public_price
        instance.wholesale_price = wholesale_price

        instance.save()
        return instance

