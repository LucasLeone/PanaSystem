"""PanaSystem statistics."""

# Django
from django.db.models import Sum, Count

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
        
        today = datetime.now().date()

        # Today's statistics
        total_earned_today = Sale.objects.filter(date__date=today).aggregate(total_earned=Sum('total'))['total_earned']
        sales_count_today = Sale.objects.filter(date__date=today).count()

        # Week's statistics
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        sales_for_week = Sale.objects.filter(date__date__range=[start_of_week, end_of_week])
        total_earned_week = sales_for_week.aggregate(total_earned=Sum('total'))['total_earned']
        sales_count_week = sales_for_week.count()

        # Month' statistics
        first_day_of_month = datetime.now().date().replace(day=1)
        last_day_of_month = first_day_of_month.replace(day=1, month=first_day_of_month.month+1) - timedelta(days=1)
        sales_for_month = Sale.objects.filter(date__date__range=[first_day_of_month, last_day_of_month])
        total_earned_month = sales_for_month.aggregate(total_earned=Sum('total'))['total_earned']
        sales_count_month = sales_for_month.count()

        # Customize's statistics
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        sales_for_period = Sale.objects.filter(date__date__range=[start_date, end_date])
        total_earned_period = sales_for_period.aggregate(total_earned=Sum('total'))['total_earned']
        sales_count_period = sales_for_period.count()

        statistics = {
            # Today
            'total_earned_today': total_earned_today or 0,
            'sales_count_today': sales_count_today or 0,

            # Week
            'total_earned_week': total_earned_week or 0,
            'sales_count_week': sales_count_week or 0,

            # Month
            'total_earned_month': total_earned_month or 0,
            'sales_count_month': sales_count_month or 0,

            # Customize
            'total_earned_period': total_earned_period or 0,
            'sales_count_period': sales_count_period or 0
        }

        return Response(statistics, status=status.HTTP_200_OK)