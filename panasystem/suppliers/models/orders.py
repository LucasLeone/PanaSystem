"""Orders models."""

# Django
from django.db import models

# Utilities
from panasystem.utils.models import PanaderiaModel
from django.utils.timezone import now


class Order(PanaderiaModel):
    """Order model."""
    
    date = models.DateTimeField(
        'Fecha',
        default=now
    )
    supplier = models.ForeignKey(
        'suppliers.Supplier',
        on_delete=models.CASCADE,
        verbose_name='Proveedor'
    )
    total = models.PositiveIntegerField()
    description = models.TextField(
        'Descripción',
        max_length=200,
        null=True,
        blank=True
    )

    def __str__(self):
        """Return Order #self.pk: $self.total"""
        return f"Order #{self.pk}: ${self.total}"
    


""" ME CONFUNDI, ESTAMOS HACIENDO UN PEDIDO A UN VIAJANTE, NADA MAS QUE ESO
class Order(PanaderiaModel):
    ""Order model.""
    
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
"""