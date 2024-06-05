"""Expenses views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

# Serializers
from panasystem.expenses.serializers import ExpenseSerializer, ExpenseCategorySerializer

# Models
from panasystem.expenses.models import Expense, ExpenseCategory
from panasystem.products.models import Product


class ExpenseViewSet(mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    """Expense viewset.
    
    Functions:
        - Create an expense.
        - List expenses:
            * Filter by 'employee, category, supplier, date'.
            * Search by 'description'.
        - Retrieve an expense.
        - Update an expense.
        - Delete an expense.
    """

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('employee', 'category', 'supplier', 'date')
    search_fields = ('description',)
    permission_classes = [IsAuthenticated]
    pagination_class = None


class ExpenseCategoryViewSet(mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """ExpenseCategory viewset.
    
    Functions:
        - Create an expense category.
        - List expense categories.
        - Retrieve an expense category.
        - Update an expense category.
        - Delete an expense category.
    """
    
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]