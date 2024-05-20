"""Customer views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Serializers
from panasystem.customers.serializers import CustomerSerializer

# Models
from panasystem.customers.models import Customer


class CustomerViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Customer view set.
    
    Functions:
        - Create a customer.
        - List customer:
            * Filter by 'is_active, afip_condition, city'.
            * Search by 'name, email, celular, address, id_number'
        - Retrieve a customer.
        - Delete a customer.
        - Update a customer.
    """
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('is_active', 'afip_condition', 'city')
    search_fields = ('name', 'email', 'celular', 'address', 'id_number')
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]