"""Customers admin."""

# Django
from django.contrib import admin

# Models
from panasystem.customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Customer admin."""

    list_display = ('pk', 'name', 'celular', 'email', 'address', 'city', 'is_active', 'created', 'modified')
    list_display_links = ('pk', 'name')