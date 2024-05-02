# Generated by Django 4.2.11 on 2024-05-02 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0011_sale_total_charged_alter_sale_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='total_charged',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Indicar cuanto se cobro por ahora.', max_digits=10, null=True, verbose_name='Total cobrado'),
        ),
    ]