# Generated by Django 4.2.11 on 2024-04-16 18:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_alter_sale_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 16, 15, 51, 26, 979162), verbose_name='Fecha'),
        ),
    ]
