"""Sales views."""

# Django REST Framework
from rest_framework import mixins, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

# Serializers
from panasystem.sales.serializers import SaleSerializer, SaleDetailSerializer

# Models
from panasystem.sales.models import Sale, SaleDetail
from panasystem.products.models import Product


class SaleViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Sale view set."""

    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def create(self, request, *args, **kwargs):
        details_data = dict(request.data).pop('details', [])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        sale_instance = serializer.instance

        is_bakery = request.data.get('is_bakery', False)

        for detail_data in details_data:
            product_id = detail_data['product']
            product = Product.objects.get(pk=product_id)
            if is_bakery and product.wholesale_price is not None:
                unit_price = product.wholesale_price
            else:
                unit_price = product.public_price

            detail_data['unit_price'] = unit_price


        sale_details_serializer = SaleDetailSerializer(data=details_data, many=True)
        sale_details_serializer.is_valid(raise_exception=True)
        sale_details_serializer.save(sale=sale_instance)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)