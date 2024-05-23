"""Expenses models."""

# Django
from django.db import models

# Utilities
from panasystem.utils.models import PanaderiaModel
from django.utils.timezone import now


class ExpenseCategory(PanaderiaModel):
    """Expense category model."""

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


class Expense(PanaderiaModel):
    """Expense model."""
    
    date = models.DateTimeField(
        'Fecha',
        default=now
    )
    
    supplier = models.ForeignKey(
        'suppliers.Supplier',
        on_delete=models.CASCADE,
        verbose_name='Proveedor',
        null=True,
        blank=True
    )

    total = models.PositiveIntegerField()

    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.CASCADE,
        verbose_name='Categoría'
    )

    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        verbose_name='Empleado'
    )
    
    description = models.TextField(
        'Descripción',
        max_length=200,
        null=True,
        blank=True
    )

    def __str__(self):
        """Return Expense #self.pk: $self.total"""
        return f"Expense #{self.pk}: ${self.total}"
    