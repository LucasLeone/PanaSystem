"""Employees models."""

# Django
from django.db import models

# Utilities
from panasystem.utils.models import PanaderiaModel


class Employee(PanaderiaModel):
    """Employee model."""
    
    name = models.CharField(
        'Nombre',
        max_length=25
    )
    
    def __str__(self):
        """Return self.name."""

        return self.name
    