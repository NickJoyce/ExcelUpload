# Generated by Django 4.1.4 on 2023-02-08 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_warehouse_supply_dates'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_added_to_main_system',
            field=models.BooleanField(default=True, verbose_name='Добавлен ли пользователь в основную систему?'),
        ),
    ]
