"""Products models."""

# Django
from django.db import models

# Utilities
from panasystem.utils.models import PanaderiaModel


class Category(PanaderiaModel):
    """Category model."""

    name = models.CharField(
        'Nombre',
        max_length=50
    )

    description = models.TextField(
        'Descripción',
        max_length=100,
        null=True,
        blank=True
    )

    def __str__(self):
        """Return name."""
        return self.name
    

class Brand(PanaderiaModel):
    """Brand model."""

    name = models.CharField(
        'Nombre',
        max_length=50
    )

    description = models.TextField(
        'Descripción',
        max_length=100,
        null=True,
        blank=True
    )

    def __str__(self):
        """Return name."""
        return self.name


class Product(PanaderiaModel):
    """Product model."""

    barcode = models.CharField(
        'Codigo de Barras',
        max_length=50,
        null=True,
        blank=True,
        unique=True
    )

    name = models.CharField(
        'Nombre',
        max_length=50
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name = 'Categoria'
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

    brand = models.ForeignKey(
        Brand,
        null=True,
        blank=True,
        verbose_name='Marca',
        on_delete=models.CASCADE
    )

    description = models.TextField(
        'Descripción',
        null=True,
        blank=True,
        max_length=100
    )

    supplier = models.ForeignKey(
        'suppliers.Supplier',
        verbose_name = 'Proveedor',
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True
    )

    current_stock = models.PositiveSmallIntegerField(
        'Stock actual',
        blank=True,
        null=True
    )

    def update_price(self, public_price, wholesale_price):
        """Update price and create price history."""
        self.public_price = public_price
        self.wholesale_price = wholesale_price
        PriceHistory.objects.create(product=self, public_price=public_price, wholesale_price=wholesale_price)
        self.save()

    def update_stock(self, quantity):
        """Update current stock after creating a sale."""
        if self.current_stock is not None:
            if self.current_stock >= quantity:
                self.current_stock -= quantity
                self.save()
            else:
                raise ValueError("Stock insuficiente para actualizar.")
        
    def get_brand_name(self):
        """Get brand name."""
        return self.brand.name if self.brand else None

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

    public_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    wholesale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    class Meta:
        """Meta options."""
        ordering = ['-created']