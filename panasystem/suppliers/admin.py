"""Suppliers admin."""

# Django
from django.contrib import admin

# Model
from panasystem.suppliers.models import Supplier, Order


admin.site.register(Supplier)
admin.site.register(Order)