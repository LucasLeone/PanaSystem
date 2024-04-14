"""Products models."""

# Django
from django.db import models

# Utilities
from panasystem.utils.models import PanaderiaModel
from django.utils import timezone


class Category(PanaderiaModel):
    """Category model."""

    name = models.CharField(
        'Nombre',
        max_length=50
    )

    def __str__(self):
        """Return name."""
        return self.name


class Product(PanaderiaModel):
    """Product model."""

    code = models.CharField(
        'Codigo de Barras',
        max_length=50,
        null=True,
        blank=True
    )
    name = models.CharField(
        'Nombre',
        max_length=50
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    public_price = models.DecimalField(
        'Precio al público',
        max_digits=10,
        decimal_places=2
    )
    wholesale_price = models.DecimalField(
        'Precio al por mayor',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    def update_price(self, new_price, wholesale=False):
        """Update price and create price history."""
        if wholesale:
            self.wholesale_price = new_price
            PriceHistory.objects.create(product=self, price=new_price, wholesale=True)
        else:
            self.public_price = new_price
            PriceHistory.objects.create(product=self, price=new_price, wholesale=False)
        self.save()

    def __str__(self):
        """Return name."""
        return self.name


class PriceHistory(PanaderiaModel):
    """Price history model."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="price_history"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    wholesale = models.BooleanField(default=False)
    date_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        """Meta options."""
        ordering = ['-date_updated']