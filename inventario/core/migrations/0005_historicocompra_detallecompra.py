# Generated by Django 5.0.7 on 2024-07-19 06:37

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_producto_descripcion_producto_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricoCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_compra', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_compra', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producto_id', models.IntegerField()),
                ('nombre_producto', models.CharField(max_length=255)),
                ('precio_unitario', models.FloatField()),
                ('cantidad', models.IntegerField()),
                ('total_producto', models.FloatField()),
                ('historico_compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='core.historicocompra')),
            ],
        ),
    ]
