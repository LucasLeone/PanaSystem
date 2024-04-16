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
    celular = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
    email = models.EmailField(
        max_length=50,
        blank=True,
        null=True
    )    
    address = models.CharField(
        'Dirección',
        max_length=30,
        blank=True,
        null=True
    )
    city = models.CharField(
        'Ciudad',
        max_length=20,
        blank=True,
        null=True
    )
    afip_condition = models.CharField(
        'Condición frente al IVA',
        max_length=75,
        blank=True,
        null=True
    )
    id_type = models.CharField(
        'Tipo de documento',
        max_length=20,
        blank=True,
        null=True
    )
    id_number = models.CharField(
        'Número de documento',
        max_length=20,
        blank=True,
        null=True
    )
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
    