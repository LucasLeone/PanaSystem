"""Customers URL's"""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views


router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls))
]