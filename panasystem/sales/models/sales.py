"""Sales models."""

# Django
from django.db import models

# Utilities
from panasystem.utils.models import PanaderiaModel
from django.utils.timezone import now


PAYMENT_METHODS = (
    ('Efectivo', 'Efectivo'),
    ('Transferencia','Transferencia'),
    ('Tarjeta', 'Tarjeta de Debito/Credito'),
    ('QR', 'QR')
)


class Sale(PanaderiaModel):
    """Sale model."""

    date = models.DateTimeField(
        'Fecha',
        default=now,
        db_index=True
    )
    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Cliente',
        related_name='customer',
        db_index=True
    )
    is_bakery = models.BooleanField(
        'Venta de panaderia',
        default=False,
        help_text="Si es venta de panaderia, el precio a utilizar es el de mayorista.",
        db_index=True
    )
    payment_method = models.CharField(
        'Método de pago',
        choices=PAYMENT_METHODS,
        default="Efectivo",
        max_length=14,
        db_index=True
    )
    total = models.DecimalField(
        'Total',
        max_digits=10,
        decimal_places=2,
        null=True, 
        blank=True,
        db_index=True
    )
    total_charged = models.DecimalField(
        'Total cobrado',
        max_digits=10,
        decimal_places=2,
        null=True, 
        blank=True,
        help_text='Indicar cuanto se cobro por ahora.'
    )
    delivered = models.BooleanField(
        'Entregado',
        default=True,
        db_index=True
    )

    @property
    def total_help(self):
        if self.total is None:
            self.total = sum(detail.subtotal for detail in self.sale_details.all())
            self.save()
        return None
    
    def save(self, *args, **kwargs):
        """Save total charged if it's null."""
        if self.total_charged == None:
            self.total_charged = self.total
        super().save(*args, **kwargs)
    
    def __str__(self):
        """Return #pk + date + total."""
        return f'Sale #{self.pk} - {self.date} - ${self.total}'


class SaleDetail(PanaderiaModel):
    """Sale detail model."""

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='sale_details'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='details_product'
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def save(self, *args, **kwargs):
        """Save unit price and subtotal."""
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)