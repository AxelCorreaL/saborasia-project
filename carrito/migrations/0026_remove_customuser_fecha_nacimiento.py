# Generated by Django 5.0.6 on 2024-05-16 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0025_remove_detallepedido_estado_pedidos_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='fecha_nacimiento',
        ),
    ]
