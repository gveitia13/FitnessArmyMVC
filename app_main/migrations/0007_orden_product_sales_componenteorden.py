# Generated by Django 4.2 on 2023-04-23 20:20

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0006_subscriptor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('link_de_pago', models.CharField(blank=True, max_length=500, null=True)),
                ('total', models.FloatField(default=0, verbose_name='Importe total')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('1', 'Completada'), ('2', 'Pendiente'), ('3', 'Cancelada')], default='2', max_length=10, verbose_name='Estado')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha')),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('phone_number', models.CharField(blank=True, max_length=200, null=True, verbose_name='Teléfono')),
                ('email', models.EmailField(max_length=254, verbose_name='Correo')),
                ('address', models.CharField(max_length=900, verbose_name='Dirección')),
            ],
            options={
                'verbose_name': 'Orden',
                'verbose_name_plural': 'Ordenes',
                'ordering': ('-date_created', '-status'),
            },
        ),
        migrations.AddField(
            model_name='product',
            name='sales',
            field=models.PositiveIntegerField(default=0, verbose_name='Ventas'),
        ),
        migrations.CreateModel(
            name='ComponenteOrden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respaldo', models.FloatField()),
                ('cantidad', models.IntegerField()),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='componente_orden', to='app_main.orden')),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='componente_producto', to='app_main.product')),
            ],
            options={
                'verbose_name': 'Componente de orden',
                'verbose_name_plural': 'Componentes de órdenes',
                'ordering': ('orden', 'producto'),
            },
        ),
    ]