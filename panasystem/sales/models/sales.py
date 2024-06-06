"""Sales models."""

# Django
from django.db import models

# Utilities
from panasystem.utils.models import PanaderiaModel
from django.utils.timezone import now


class Sale(PanaderiaModel):
    """Sale model."""

    PAYMENT_METHOD_CASH = 'efv'
    PAYMENT_METHOD_TRANSFER = 'trf'
    PAYMENT_METHOD_CARD = 'crd'
    PAYMENT_METHOD_QR = 'qr'

    PAYMENT_METHODS = (
        (PAYMENT_METHOD_CASH, 'Efectivo'),
        (PAYMENT_METHOD_TRANSFER, 'Transferencia'),
        (PAYMENT_METHOD_CARD, 'Tarjeta de Débito/Crédito'),
        (PAYMENT_METHOD_QR, 'QR')
    )

    date = models.DateTimeField('Fecha', default=now)

    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Cliente',
        related_name='sales'
    )

    is_bakery = models.BooleanField(
        'Venta de panadería',
        default=False,
        help_text="Si es venta de panadería, el precio a utilizar es el de mayorista."
    )

    payment_method = models.CharField(
        'Método de pago',
        choices=PAYMENT_METHODS,
        default=PAYMENT_METHOD_CASH,
        max_length=3
    )

    total = models.DecimalField(
        'Total',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    total_charged = models.DecimalField(
        'Total cobrado',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Indicar cuánto se cobró por ahora.'
    )

    delivered = models.BooleanField(
        'Entregado',
        default=True
    )

    def calculate_total(self):
        """Calculate the total from sale details if details exist."""
        if self.sale_details.exists():
            self.total = sum(detail.subtotal for detail in self.sale_details.all())
        self.save()

    def save(self, *args, **kwargs):
        """Save total charged if it's null."""
        if self.total_charged is None:
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

    def __str__(self):
        """Return product name and quantity."""
        return f'{self.product.name} - {self.quantity}'
