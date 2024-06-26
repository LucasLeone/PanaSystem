# Generated by Django 4.2.11 on 2024-04-16 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created.', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the object was last modified.', verbose_name='modified at')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('celular', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(blank=True, max_length=30, null=True, verbose_name='Dirección')),
                ('city', models.CharField(blank=True, max_length=20, null=True, verbose_name='Ciudad')),
                ('afip_condition', models.CharField(blank=True, max_length=75, null=True, verbose_name='Condición frente al IVA')),
                ('id_type', models.CharField(blank=True, max_length=20, null=True, verbose_name='Tipo de documento')),
                ('id_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Número de documento')),
                ('is_active', models.BooleanField(default=True, help_text='Indica si el cliente esta activo', verbose_name='Activo')),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
