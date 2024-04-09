import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductsConfig(AppConfig):
    name = "panasystem.products"
    verbose_name = _("products")

    def ready(self):
        with contextlib.suppress(ImportError):
            import panasystem.products.signals  # noqa: F401
