"""Products admin."""

# Django
from django.contrib import admin

# Model
from panasystem.products.models.products import Product, PriceHistory, Category, Brand


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product admin."""

    list_display = (
        'pk',
        'code',
        'name',
        'category',
        'supplier',
        'brand',
        'public_price',
        'wholesale_price',
        'description'
    )

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    """Price history admin."""

    list_display = (
        'pk',
        'product',
        'public_price',
        'wholesale_price',
        'created',
        'modified'
    )

admin.site.register(Category)
admin.site.register(Brand)