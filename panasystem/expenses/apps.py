import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExpensesConfig(AppConfig):
    name = "panasystem.expenses"
    verbose_name = _("Expenses")

    def ready(self):
        with contextlib.suppress(ImportError):
            import panasystem.expenses.signals  # noqa: F401
