# Generated by Django 5.0.6 on 2024-05-15 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0011_customuser_alter_carrito_usuario_delete_usuarios'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]