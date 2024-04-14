"""Customers models."""

# Django
from django.db import models

# Utilities
from panasystem.utils.models import PanaderiaModel


class Customer(PanaderiaModel):
    """Customer model."""

    name = models.CharField(
        'Nombre',
        max_length=50
    )
    celular = models.CharField(max_length=15)
    address = models.CharField(max_length=30)
    city = models.CharField(max_lenght=20)
    is_active = models.BooleanField(
        'Activo',
        default=True,
        help_text="Indica si el cliente esta activo",
        null=False,
        editable=True
    )

    def __str__(self):
        """Return name."""
        return self.name
    