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
        default=now
    )
    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Cliente',
        related_name='customer'
    )
    is_bakery = models.BooleanField(
        'Venta de panaderia',
        default=False,
        help_text="Si es venta de panaderia, el precio a utilizar es el de mayorista."
    )
    payment_method = models.CharField(
        'Método de pago',
        choices=PAYMENT_METHODS,
        default="Efectivo",
        max_length=14
    )
    total = models.DecimalField(
        'Total calculado',
        max_digits=10,
        decimal_places=2,
        null=True, 
        blank=True
    )
    delivered = models.BooleanField(
        'Entregado',
        default=True
    )

    @property
    def total_help(self):
        if self.total is None:
            self.total = sum(detail.subtotal for detail in self.sale_details.all())
        return None


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