"""PanaSystem statistics."""

# Django
from django.db.models import Sum

# Django REST Framework
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# Models
from panasystem.sales.models import Sale, SaleDetail
from panasystem.products.models import Product
from panasystem.suppliers.models import Order

# Utilities
from datetime import datetime, timedelta


class Statistics(viewsets.ViewSet):
    """PanaSystem statistics.
    
    Functions:
        - Show sales for today, current week and month.
        - Filter by payment_method for each one.
    """

    def list(self, request):
        """Get the JSON."""

        statistics = {
            'sales_today': self.get_sales_statistics_for_today(request),
            'sales_week': self.get_sales_statistics_for_week(request),
            'sales_month': self.get_sales_statistics_for_month(request),
            'sales_custom': self.get_sales_custom_statistics(request),
        }
        return Response(statistics, status=status.HTTP_200_OK)

    def get_sales_statistics_for_today(self, request):
        """Get sales statistics' for today."""

        today = datetime.now().date()
        payment_method_today = request.query_params.get("payment_method_today")
        sales_for_today = Sale.objects.filter(date__date=today)
        if payment_method_today:
            sales_for_today = sales_for_today.filter(payment_method=payment_method_today)
        total_earned_today = sales_for_today.aggregate(total_earned=Sum('total'))['total_earned']
        sales_count_today = sales_for_today.count()
        total_orders_today = Order.objects.filter(date__date=today).aggregate(total_earned=Sum('total'))['total_earned']

        best_selling_products = self.get_best_selling_products(today, today + timedelta(days=1))
        
        return {
            'total_earned_today': total_earned_today or 0,
            'sales_count_today': sales_count_today or 0,
            'best_selling_products': best_selling_products,
            'total_orders_today': total_orders_today
        }

    def get_sales_statistics_for_week(self, request):
        """Get sales statistics' for this week."""
        
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        payment_method_week = request.query_params.get('payment_method_week')
        sales_for_week = Sale.objects.filter(date__date__range=[start_of_week, end_of_week])
        if payment_method_week:
            sales_for_week = sales_for_week.filter(payment_method=payment_method_week)
        total_earned_week = sales_for_week.aggregate(total_earned=Sum('total'))['total_earned']
        sales_count_week = sales_for_week.count()
        best_selling_products = self.get_best_selling_products(start_of_week, end_of_week)
        total_orders_week = Order.objects.filter(date__date__range=[start_of_week, end_of_week]).aggregate(total_earned=Sum('total'))['total_earned']

        return {
            'total_earned_week': total_earned_week or 0,
            'sales_count_week': sales_count_week or 0,
            'best_selling_products': best_selling_products,
            'total_orders_week': total_orders_week
        }

    def get_sales_statistics_for_month(self, request):
        """Get sales statistics' for this month."""

        today = datetime.now().date()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = first_day_of_month.replace(day=1, month=first_day_of_month.month+1) - timedelta(days=1)
        payment_method_month = request.query_params.get('payment_method_month')
        sales_for_month = Sale.objects.filter(date__date__range=[first_day_of_month, last_day_of_month])
        if payment_method_month:
            sales_for_month = sales_for_month.filter(payment_method=payment_method_month)
        total_earned_month = sales_for_month.aggregate(total_earned=Sum('total'))['total_earned']
        sales_count_month = sales_for_month.count()
        best_selling_products = self.get_best_selling_products(first_day_of_month, last_day_of_month)
        total_orders_month = Order.objects.filter(date__date__range=[first_day_of_month, last_day_of_month]).aggregate(total_earned=Sum('total'))['total_earned']
        
        return {
            'total_earned_month': total_earned_month or 0,
            'sales_count_month': sales_count_month or 0,
            'best_selling_products': best_selling_products,
            'total_orders_month': total_orders_month
        }

    def get_sales_custom_statistics(self, request):
        """Get sales statistics' for a period."""

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        payment_method_customize = request.query_params.get('payment_method_customize')
        sales_for_period = Sale.objects.filter(date__date__range=[start_date, end_date])
        if payment_method_customize:
            sales_for_period = sales_for_period.filter(payment_method=payment_method_customize)
        total_earned_period = sales_for_period.aggregate(total_earned=Sum('total'))['total_earned']
        sales_count_period = sales_for_period.count()
        best_selling_products = self.get_best_selling_products(start_date, end_date)
        total_orders_period = Order.objects.filter(date__date__range=[start_date, end_date]).aggregate(total_earned=Sum('total'))['total_earned']

        return {
            'total_earned_period': total_earned_period or 0,
            'sales_count_period': sales_count_period or 0,
            'best_selling_products': best_selling_products,
            'total_orders_period': total_orders_period
        }
    
    def get_best_selling_products(self, start_date=None, end_date=None):
        """Get the best selling products."""
        
        if start_date and end_date:
            sales = SaleDetail.objects.filter(sale__date__range=[start_date, end_date])
            best_selling_product_ids = sales.values('product').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]

            best_selling_products = Product.objects.filter(id__in=[product['product'] for product in best_selling_product_ids])
            result = []
            for product in best_selling_products:
                total_quantity = next(item['total_quantity'] for item in best_selling_product_ids if item['product'] == product.id)

                result.append({
                    'product_name': product.name,
                    'total_quantity_sold': total_quantity
                })
            return result
        else:
            return 0
