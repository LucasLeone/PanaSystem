"""Sales views."""

# Django REST Framework
from rest_framework import mixins, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

# Serializers
from panasystem.sales.serializers import SaleSerializer, SaleDetailSerializer

# Models
from panasystem.sales.models import Sale
from panasystem.products.models import Product

# Utilities
from datetime import datetime, timedelta


class DateFilter(filters.Filter):
    def filter(self, queryset, value):
        if value:
            start_date = datetime.strptime(value, '%Y-%m-%d').date()
            end_date = start_date + timedelta(days=1)
            return queryset.filter(date__gte=start_date, date__lt=end_date)
        return queryset


class SaleFilter(filters.FilterSet):
    """Sale filter."""

    date_range = filters.DateFromToRangeFilter(field_name='date')
    date = DateFilter(field_name='date')

    class Meta:
        """Meta options."""

        model = Sale
        fields = ['customer', 'is_bakery', 'payment_method', 'delivered', 'date', 'date_range', 'total_charged']


class SaleViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Sale view set.
    
    Functions:
        - Create a quick sale (total only).
        - Create a detailed sale (all fields, with details).
        - Create multiple sales at once or just one.
        - List sales:
            * Filter by 'customer, is_bakery, payment_method, delivered, date, date_range'.
            * Search by customer.
            * Order by date and total.
        - Retrieve a sale
        - Delete a sale
        - Update a sale
    """

    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = SaleFilter
    search_fields = ('customer',)
    ordering_fields = ('date', 'total')
    

    def create(self, request, *args, **kwargs):
        """Create sales and sale details."""
        
        sales_data = request.data
        if not isinstance(sales_data, list):
            sales_data = [sales_data]

        created_sales = []

        for sale_data in sales_data:
            details_data = sale_data.pop('details', [])
            serializer = self.get_serializer(data=sale_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            sale_instance = serializer.instance

            is_bakery = sale_data.get('is_bakery', False)

            for detail_data in details_data:
                product_id = detail_data['product']
                product = Product.objects.get(pk=product_id)
                if is_bakery and product.wholesale_price is not None:
                    unit_price = product.wholesale_price
                else:
                    unit_price = product.public_price

                detail_data['unit_price'] = unit_price
                product.update_stock(detail_data['quantity'])

            sale_details_serializer = SaleDetailSerializer(data=details_data, many=True)
            sale_details_serializer.is_valid(raise_exception=True)
            sale_details_serializer.save(sale=sale_instance)

            created_sales.append(serializer.data)

        headers = self.get_success_headers(created_sales)
        return Response(created_sales, status=status.HTTP_201_CREATED, headers=headers)