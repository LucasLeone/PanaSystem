"""Sales admin."""

# Django
from django.contrib import admin

# Models
from panasystem.sales.models import Sale, SaleDetail


admin.site.register(SaleDetail)
admin.site.register(Sale)
