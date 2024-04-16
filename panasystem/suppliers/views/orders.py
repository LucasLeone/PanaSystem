"""Orders views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

# Serializers
from panasystem.suppliers.serializers import OrderSerializer

# Models
from panasystem.suppliers.models import Order
from panasystem.products.models import Product


class OrderViewSet(mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    """Order viewset."""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('supplier',)
    search_fields = ('description',)

    """
    def create(self, request, *args, **kwargs):
        details_data = dict(request.data).pop('details', [])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        order_instance = serializer.instance

        # Determinar si la orden es mayorista o no
        is_wholesale = request.data.get('wholesale', False)

        # Guardar los detalles de la orden
        for detail_data in details_data:
            # Determinar el precio unitario a utilizar
            product_id = detail_data['product']
            product = Product.objects.get(pk=product_id)
            if is_wholesale and product.wholesale_price is not None:
                unit_price = product.wholesale_price
            else:
                unit_price = product.public_price

            # Agregar el precio unitario a los datos del detalle de la orden
            detail_data['unit_price'] = unit_price

        order_details_serializer = OrderDetailSerializer(data=details_data, many=True)
        order_details_serializer.is_valid(raise_exception=True)
        order_details_serializer.save(order=order_instance)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        """