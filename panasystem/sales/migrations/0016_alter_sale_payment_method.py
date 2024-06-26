# Generated by Django 4.2.11 on 2024-06-06 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0015_alter_sale_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='payment_method',
            field=models.CharField(choices=[('efv', 'Efectivo'), ('trf', 'Transferencia'), ('crd', 'Tarjeta de Débito/Crédito'), ('qr', 'QR')], default='efv', max_length=3, verbose_name='Método de pago'),
        ),
    ]
