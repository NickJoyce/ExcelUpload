# Generated by Django 4.1.4 on 2023-02-08 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_custompagemodel_options_warehouse_supply_dates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='supply_dates',
            field=models.JSONField(default=[], verbose_name='Даты поставок'),
        ),
    ]
