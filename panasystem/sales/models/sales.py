"""Sales models."""

# Django
from django.db import models
from django.core.exceptions import ValidationError

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

    def clean(self):
        """Verify total and total_charged data."""
        if self.total is not None and self.total <= 0:
            raise ValidationError({'total': 'Total must be greater than 0.'})
        if self.total_charged is not None and self.total_charged < 0:
            raise ValidationError({'total_charged': 'Total charged must be equal to o greater than 0.'})

    def calculate_total(self):
        """Calculate the total from sale details if details exist."""
        if self.sale_details.exists():
            self.total = sum(detail.subtotal for detail in self.sale_details.all())
        self.save()

    def save(self, *args, **kwargs):
        """Save total charged if it's null."""
        self.full_clean()
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

    def clean(self):
        """Verify quantity, unit_price and subtotal data."""
        if self.quantity <= 0:
            raise ValidationError({'quantity': 'Quantity must be greater than 0.'})
        if self.unit_price <= 0:
            raise ValidationError({'unit_price': 'Unit price must be greater than 0.'})
        if self.subtotal is not None:
            if self.subtotal <= 0:
                raise ValidationError({'subtotal': 'Subtotal must be greater than 0.'})

    def save(self, *args, **kwargs):
        """Save unit price and subtotal."""
        self.full_clean()
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        """Return product name and quantity."""
        return f'{self.product.name} - {self.quantity}'
