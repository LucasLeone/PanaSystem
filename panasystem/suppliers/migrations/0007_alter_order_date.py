# Generated by Django 4.2.11 on 2024-04-15 23:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0006_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 15, 20, 46, 37, 348153), verbose_name='Fecha'),
        ),
    ]
