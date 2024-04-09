import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SuppliersConfig(AppConfig):
    name = "panasystem.suppliers"
    verbose_name = _("Suppliers")

    def ready(self):
        with contextlib.suppress(ImportError):
            import panasystem.suppliers.signals  # noqa: F401
