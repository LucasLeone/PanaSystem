import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SalesConfig(AppConfig):
    name = "panasystem.sales"
    verbose_name = _("Sales")

    def ready(self):
        with contextlib.suppress(ImportError):
            import panasystem.sales.signals  # noqa: F401
