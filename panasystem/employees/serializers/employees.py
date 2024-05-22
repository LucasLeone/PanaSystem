"""Employees serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from panasystem.employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """Employee serializer."""

    class Meta:
        """Meta options."""

        model = Employee
        fields = '__all__'