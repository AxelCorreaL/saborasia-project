# Generated by Django 5.0.6 on 2024-05-13 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0003_alter_usuarios_num_tarjeta_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='direccion_envio',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='fecha_nacimiento',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='nombre',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='primer_apellido',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
