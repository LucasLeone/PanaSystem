"""Sales views."""

# Django
from django.db.models import F

# Django REST Framework
from rest_framework import mixins, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action

# Serializers
from panasystem.sales.serializers import SaleSerializer, SaleDetailSerializer

# Models
from panasystem.sales.models import Sale
from panasystem.products.models import Product

# Utilities
from datetime import datetime, timedelta
from django.db import transaction
from django.db.models import Sum


class DateFilter(filters.Filter):
    """Custom filter to filter by exact date."""

    def filter(self, queryset, value):
        """Filter queryset by exact date."""
        if value:
            start_date = datetime.strptime(value, '%Y-%m-%d').date()
            end_date = start_date + timedelta(days=1)
            return queryset.filter(date__gte=start_date, date__lt=end_date)
        return queryset


class SaleFilter(filters.FilterSet):
    """Sale filter for filtering sales based on different criteria."""

    date_range = filters.DateFromToRangeFilter(field_name='date')
    date = DateFilter(field_name='date')
    uncharged = filters.BooleanFilter(method='filter_uncharged')

    class Meta:
        """Meta options for SaleFilter."""
        model = Sale
        fields = ['customer', 'is_bakery', 'payment_method', 'delivered', 'date', 'date_range', 'uncharged']

    def filter_uncharged(self, queryset, name, value):
        """Filter sales where total_charged is less than total."""
        if value:
            return queryset.filter(total_charged__lt=F('total'))
        return queryset


class SaleViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    ViewSet for managing sales.

    Provides the following actions:
    - Create a sale or multiple sales in a single request
    - List sales with filters by 'customer', 'is_bakery', 'payment_method', 'delivered', 'date', 'date_range', 'total_charged'
    - Search sales by 'customer name'
    - Order sales by 'date' or 'total'
    - Retrieve a specific sale
    - Update a sale's details
    - Delete a sale

    Permissions:
    - Requires the user to be authenticated to perform any action.
    """

    queryset = Sale.objects.all().select_related('customer').prefetch_related('sale_details__product')
    serializer_class = SaleSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = SaleFilter
    search_fields = ('customer__name',)
    ordering_fields = ('date', 'total')
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        """Create one or multiple sales in a single request."""
        sales_data = request.data

        if not isinstance(sales_data, list):
            sales_data = [sales_data]

        created_sales = []

        with transaction.atomic():
            for sale_data in sales_data:
                details_data = sale_data.pop('sale_details', [])
                serializer = self.get_serializer(data=sale_data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                sale_instance = serializer.instance

                is_bakery = sale_instance.is_bakery

                for detail_data in details_data:
                    product_id = detail_data['product']
                    try:
                        product = Product.objects.get(pk=product_id)
                    except Product.DoesNotExist:
                        raise ValidationError(f"Product with id {product_id} does not exist.")

                    if is_bakery and product.wholesale_price is not None:
                        unit_price = product.wholesale_price
                    else:
                        unit_price = product.public_price

                    detail_data['unit_price'] = unit_price
                    product.update_stock(detail_data['quantity'])

                sale_details_serializer = SaleDetailSerializer(data=details_data, many=True)
                sale_details_serializer.is_valid(raise_exception=True)
                sale_details_serializer.save(sale=sale_instance)

                sale_instance.calculate_total()
                created_sales.append(serializer.data)

        headers = self.get_success_headers(created_sales)
        return Response(created_sales, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def totals(self, request, *args, **kwargs):
        """
        Get total sales and sum of totals.

        Required query parameters:
        - date_from: start date for the range (YYYY-MM-DD)
        - date_to: end date for the range (YYYY-MM-DD)

        Optional query parameters:
        - is_bakery: filter by whether the sale is bakery-related (true/false)
        - payment_method: filter by payment method

        Example: api/v1/sales/totals/?date_from=2024-01-01&date_to=2024-12-31&is_bakery=false&payment_method=efv

        List of payment methods:
        - efv ('Efectivo' -> Cash in English)
        - trf ('Transferencia' -> Transfer in English)
        - crd ('Tarjeta de Crédito/Débito' -> Credit/Debit card in English)
        - qr ('QR')
        """
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        payment_method = request.query_params.get('payment_method')
        is_bakery = request.query_params.get('is_bakery')

        # Verify the existence of parameters.
        if not date_from or not date_to:
            return Response({"error": "date_from and date_to parameters are required (is_bakery and payment_method are optional)."}, status=status.HTTP_400_BAD_REQUEST)

        # Convert dates to a valid format.
        try:
            start_date = datetime.strptime(date_from, '%Y-%m-%d').date()
            end_date = datetime.strptime(date_to, '%Y-%m-%d').date() + timedelta(days=1)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = Sale.objects.filter(date__gte=start_date, date__lt=end_date)
        
        # Convert 'is_bakery' to boolean.
        if is_bakery is not None:
            if isinstance(is_bakery, bool):
                is_bakery = is_bakery
            elif is_bakery.lower() in ['true', '1', 'yes']:
                is_bakery = True
            elif is_bakery.lower() in ['false', '0', 'no']:
                is_bakery = False
            else:
                return Response({"error": "Invalid value for is_bakery. Use 'true' or 'false'."}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(is_bakery=is_bakery)

        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)

        total_sales = queryset.count()
        sum_total = queryset.aggregate(Sum('total'))['total__sum'] or 0

        return Response({
            "total_sales": total_sales,
            "sum_total": sum_total
        })