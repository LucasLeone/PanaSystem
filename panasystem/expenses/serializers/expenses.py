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
    supplier = serializers.SlugRelatedField(slug_field='name', queryset=Supplier.objects.all(), required=False)
    employee = serializers.SlugRelatedField(slug_field='name', queryset=Employee.objects.all())

    class Meta:
        model = Expense
        fields = '__all__'