"""Employees admin."""

# Django
from django.contrib import admin

# Models
from panasystem.employees.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Employee admin."""

    list_display = ('pk', 'name')