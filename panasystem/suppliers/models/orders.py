"""Orders models."""

# Django
from django.db import models

# Utilities
from panasystem.utils.models import PanaderiaModel
from django.utils import timezone
from datetime import datetime


class Order(PanaderiaModel):
    """Order model."""
    
    date = models.DateTimeField(
        'Fecha',
        default=datetime.now()
    )
    supplier = models.ForeignKey(
        'suppliers.Supplier',
        on_delete=models.CASCADE,
        verbose_name='Proveedor'
    )
    payment_method = models.CharField(max_length=50)
    wholesale = models.BooleanField(
        'Venta mayorista',
        default=False
    )

    @property
    def total(self):
        return sum(detail.subtotal for detail in self.details.all())
    
class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='details',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)