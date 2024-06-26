# Generated by Django 4.2.11 on 2024-06-06 09:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_customer_options_and_more'),
        ('sales', '0013_alter_sale_date_alter_sale_delivered_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='customers.customer', verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='delivered',
            field=models.BooleanField(default=True, verbose_name='Entregado'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='is_bakery',
            field=models.BooleanField(default=False, help_text='Si es venta de panadería, el precio a utilizar es el de mayorista.', verbose_name='Venta de panadería'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='payment_method',
            field=models.CharField(choices=[('efv', 'Efectivo'), ('trf', 'Transferencia'), ('crd', 'Tarjeta de Débito/Crédito'), ('qr', 'QR')], default='efv', max_length=3, verbose_name='Método de pago'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='total_charged',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Indicar cuánto se cobró por ahora.', max_digits=10, null=True, verbose_name='Total cobrado'),
        ),
    ]
