# Generated by Django 5.0.6 on 2024-05-14 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0007_alter_carrito_id_carrito_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='rutaImg',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
