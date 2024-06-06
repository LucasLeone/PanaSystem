"""Employees views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

# Serializers
from panasystem.employees.serializers import EmployeeSerializer

# Models
from panasystem.employees.models import Employee


class EmployeeViewSet(mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    """Employee viewset.
    
    Functions:
        - Create an employee.
        - List employees:
            * Search by 'name'.
        - Retrieve an employee.
        - Update an employee.
        - Delete an employee.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAuthenticated]
    pagination_class = None
