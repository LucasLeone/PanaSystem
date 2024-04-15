"""Suppliers models."""

# Django
from django.db import models

# Utilities
from panasystem.utils.models import PanaderiaModel


class Supplier(PanaderiaModel):
    """Supplier model."""

    name = models.CharField(
        max_length=50,
        verbose_name="Nombre",
    )
    celular = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    def __str__(self):
        """Return name."""
        return self.name
    