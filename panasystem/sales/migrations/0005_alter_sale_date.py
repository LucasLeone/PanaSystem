# Generated by Django 4.2.11 on 2024-04-16 18:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_alter_sale_date_alter_saledetail_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 16, 15, 50, 18, 831182), verbose_name='Fecha'),
        ),
    ]
