import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmployeesConfig(AppConfig):
    name = "panasystem.employees"
    verbose_name = _("Employees")

    def ready(self):
        with contextlib.suppress(ImportError):
            import panasystem.employees.signals  # noqa: F401
