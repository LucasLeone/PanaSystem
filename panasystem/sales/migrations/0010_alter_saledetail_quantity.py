# Generated by Django 4.2.11 on 2024-04-17 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0009_alter_sale_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saledetail',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
