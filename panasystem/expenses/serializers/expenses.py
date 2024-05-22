"""Expenses serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from panasystem.expenses.models import Expense, ExpenseCategory
from panasystem.suppliers.models import Supplier
from panasystem.employees.models import Employee


class ExpenseCategorySerializer(serializers.ModelSerializer):
    """Expense category serializer."""

    class Meta:
        model = ExpenseCategory
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer for expense."""

    category = serializers.SlugRelatedField(slug_field='name', queryset=ExpenseCategory.objects.all())
    supplier = serializers.SlugRelatedField(slug_field='name', queryset=Supplier.objects.all())
    employee = serializers.SlugRelatedField(slug_field='name', queryset=Employee.objects.all())

    class Meta:
        model = Expense
        fields = '__all__'

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category = ExpenseCategory.objects.create(**category_data)
        expense = Expense.objects.create(category=category, **validated_data)
        return expense

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category')
        instance.category.name = category_data.get('name', instance.category.name)
        instance.category.description = category_data.get('description', instance.category.description)
        instance.category.save()

        instance.date = validated_data.get('date', instance.date)
        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.total = validated_data.get('total', instance.total)
        instance.employee = validated_data.get('employee', instance.employee)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance