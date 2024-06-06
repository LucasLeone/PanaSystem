# Django
from django.conf import settings
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

# Views
from panasystem.products.views import ProductViewSet, ProductCategoryViewSet, ProductBrandViewSet
from panasystem.suppliers.views import SuppliersViewSet
from panasystem.customers.views import CustomerViewSet
from panasystem.sales.views import SaleViewSet
from panasystem.expenses.views import ExpenseViewSet, ExpenseCategoryViewSet
from panasystem.employees.views import EmployeeViewSet
from panasystem.users.views import UsersViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("products", ProductViewSet)
router.register("product-brands", ProductBrandViewSet)
router.register("product-categories", ProductCategoryViewSet)
router.register("suppliers", SuppliersViewSet)
router.register("customers", CustomerViewSet)
router.register("sales", SaleViewSet)
router.register("expenses", ExpenseViewSet)
router.register("expense-categories", ExpenseCategoryViewSet)
router.register("employees", EmployeeViewSet)
router.register("users", UsersViewSet, basename='users')

app_name = "api"
urlpatterns = router.urls