"""Sales admin."""

# Django
from django.contrib import admin

# Models
from panasystem.sales.models import Sale, SaleDetail


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """Sale admin."""

    list_display = (
        'pk', 'date', 'customer',
        'is_bakery', 'payment_method',
        'total', 'delivered', 'created'
    )

admin.site.register(SaleDetail)
