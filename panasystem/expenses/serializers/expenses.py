"""Expenses serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from panasystem.expenses.models import Expense, ExpenseCategory
from panasystem.suppliers.models import Supplier
from panasystem.employees.models import Employee


class ExpenseCategorySerializer(serializers.ModelSerializer):
    """Expense category model serializer."""

    class Meta:
        model = ExpenseCategory
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    """Expense model serializer."""

    category = serializers.PrimaryKeyRelatedField(queryset=ExpenseCategory.objects.all())
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), required=False)
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = Expense
        fields = '__all__'

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        supplier_data = validated_data.pop('supplier', None)
        employee_data = validated_data.pop('employee')
        
        expense = Expense.objects.create(
            category=category_data,
            supplier=supplier_data,
            employee=employee_data,
            **validated_data
        )
        return expense

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.employee = validated_data.get('employee', instance.employee)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
