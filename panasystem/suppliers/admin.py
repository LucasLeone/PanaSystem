"""Suppliers admin."""

# Django
from django.contrib import admin

# Model
from panasystem.suppliers.models import Supplier


admin.site.register(Supplier)