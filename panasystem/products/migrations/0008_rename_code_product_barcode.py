# Generated by Django 4.2.11 on 2024-06-05 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_product_current_stock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='code',
            new_name='barcode',
        ),
    ]
