# Generated by Django 5.0.6 on 2024-05-16 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0016_alter_customuser_managers_alter_customuser_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=255),
        ),
    ]
