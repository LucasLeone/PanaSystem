"""PanaSystem statistics."""

# Django
from django.db.models import Sum

# Django REST Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Models
from panasystem.sales.models import Sale

# Utilities
from datetime import datetime, timedelta


class SalesStatistics(APIView):
    """Sales statistics."""

    def get(self, request, format=None):
        statistics = {
            'today': self.get_statistics_for_today(request),
            'week': self.get_statistics_for_week(request),
            'month': self.get_statistics_for_month(request),
            'custom': self.get_custom_statistics(request),
        }
        return Response(statistics, status=status.HTTP_200_OK)

    def get_statistics_for_today(self, request):
        today = datetime.now().date()
        payment_method_today = request.query_params.get("payment_method_today")
        sales_for_today = Sale.objects.filter(date__date=today)
        if payment_method_today:
            sales_for_today = sales_for_today.filter(payment_method=payment_method_today)
        total_earned_today = sales_for_today.aggregate(total_earned=Sum('total'))['total_earned']
        sales_count_today = sales_for_today.count()
        return {
            'total_earned_today': total_earned_today or 0,
            'sales_count_today': sales_count_today or 0,
        }

    def get_statistics_for_week(self, request):
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        payment_method_week = request.query_params.get('payment_method_week')
        sales_for_week = Sale.objects.filter(date__date__range=[start_of_week, end_of_week])
        if payment_method_week:
            sales_for_week = sales_for_week.filter(payment_method=payment_method_week)
        total_earned_week = sales_for_week.aggregate(total_earned=Sum('total'))['total_earned']
        sales_count_week = sales_for_week.count()
        return {
            'total_earned_week': total_earned_week or 0,
            'sales_count_week': sales_count_week or 0,
        }

    def get_statistics_for_month(self, request):
        today = datetime.now().date()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = first_day_of_month.replace(day=1, month=first_day_of_month.month+1) - timedelta(days=1)
        payment_method_month = request.query_params.get('payment_method_month')
        sales_for_month = Sale.objects.filter(date__date__range=[first_day_of_month, last_day_of_month])
        if payment_method_month:
            sales_for_month = sales_for_month.filter(payment_method=payment_method_month)
        total_earned_month = sales_for_month.aggregate(total_earned=Sum('total'))['total_earned']
        sales_count_month = sales_for_month.count()
        return {
            'total_earned_month': total_earned_month or 0,
            'sales_count_month': sales_count_month or 0,
        }

    def get_custom_statistics(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        payment_method_customize = request.query_params.get('payment_method_customize')
        sales_for_period = Sale.objects.filter(date__date__range=[start_date, end_date])
        if payment_method_customize:
            sales_for_period = sales_for_period.filter(payment_method=payment_method_customize)
        total_earned_period = sales_for_period.aggregate(total_earned=Sum('total'))['total_earned']
        sales_count_period = sales_for_period.count()
        return {
            'total_earned_period': total_earned_period or 0,
            'sales_count_period': sales_count_period or 0,
        }
