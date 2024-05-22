"""Expenses admin."""

# Django
from django.contrib import admin

# Models
from panasystem.expenses.models import Expense, ExpenseCategory


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """Expense admin."""

    list_display = ('pk', 'date', 'supplier', 'total', 'category', 'employee')


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    """Expense category admin."""

    list_display = ('pk', 'name', 'description')