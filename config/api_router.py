# Django
from django.conf import settings
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

# Views
from panasystem.products.views import ProductViewSet, CategoryViewSet, BrandViewSet
from panasystem.suppliers.views import OrderViewSet, SuppliersViewSet
from panasystem.customers.views import CustomerViewSet
from panasystem.sales.views import SaleViewSet
from panasystem.expenses.views import ExpenseViewSet, ExpenseCategoryViewSet
from panasystem.employees.views import EmployeeViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)
router.register("orders", OrderViewSet)
router.register("suppliers", SuppliersViewSet)
router.register("brands", BrandViewSet)
router.register("customers", CustomerViewSet)
router.register("sales", SaleViewSet)
router.register("expenses", ExpenseViewSet)
router.register("expense-category", ExpenseCategoryViewSet)
router.register("employees", EmployeeViewSet)

app_name = "api"
urlpatterns = router.urls