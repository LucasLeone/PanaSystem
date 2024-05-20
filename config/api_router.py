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

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)
router.register("orders", OrderViewSet)
router.register("suppliers", SuppliersViewSet)
router.register("brands", BrandViewSet)
router.register("customers", CustomerViewSet)
router.register("sales", SaleViewSet)

app_name = "api"
urlpatterns = router.urls