# Generated by Django 4.2.11 on 2024-04-15 19:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0003_order_orderdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 15, 16, 54, 52, 566435), verbose_name='Fecha'),
        ),
    ]
