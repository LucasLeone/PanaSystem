"""Expenses views."""

# Django REST Framework
import django_filters
from rest_framework import mixins, viewsets
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

# Serializers
from panasystem.expenses.serializers import ExpenseSerializer, ExpenseCategorySerializer

# Models
from panasystem.expenses.models import Expense, ExpenseCategory

# Utilities
from datetime import datetime, timedelta


class DateFilter(django_filters.Filter):
    """Date filter.

    Modify date like "2024-06-03T18:19:10.236684" for "2024-06-03".
    """
    def filter(self, queryset, value):
        if value:
            start_date = datetime.strptime(value, '%Y-%m-%d').date()
            end_date = start_date + timedelta(days=1)
            return queryset.filter(date__gte=start_date, date__lt=end_date)
        return queryset


class ExpenseFilter(filters.FilterSet):
    """Expense filters."""

    date = DateFilter(field_name='date')

    class Meta:
        model = Expense
        fields = ['employee', 'category', 'supplier', 'date']


class ExpenseViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    ViewSet for managing expenses.

    Provides the following actions:
    - Create an expense
    - List expenses with filters by 'employee', 'category', 'supplier', and 'date', and search capability by 'description'
    - Retrieve a specific expense
    - Update an expense's details
    - Delete an expense

    Permissions:
    - Requires the user to be authenticated to perform any action.
    """

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = ExpenseFilter
    search_fields = ('description',)
    permission_classes = [IsAuthenticated]
    pagination_class = None


class ExpenseCategoryViewSet(mixins.CreateModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.ListModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    """
    ViewSet for managing expense categories.

    Provides the following actions:
    - Create an expense category
    - List expense categories
    - Retrieve a specific expense category
    - Update an expense category's details
    - Delete an expense category

    Permissions:
    - Requires the user to be authenticated to perform any action.
    """

    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]