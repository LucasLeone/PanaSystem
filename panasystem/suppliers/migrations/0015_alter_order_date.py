# Generated by Django 4.2.11 on 2024-04-16 18:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0014_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 16, 18, 50, 18, 832824, tzinfo=datetime.timezone.utc), verbose_name='Fecha'),
        ),
    ]