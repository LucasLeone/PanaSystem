# Generated by Django 4.2.11 on 2024-04-16 16:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0011_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 16, 13, 14, 13, 663178), verbose_name='Fecha'),
        ),
    ]