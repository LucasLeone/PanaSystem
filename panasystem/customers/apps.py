import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CustomersConfig(AppConfig):
    name = "panasystem.customers"
    verbose_name = _("Customers")

    def ready(self):
        with contextlib.suppress(ImportError):
            import panasystem.customers.signals  # noqa: F401
