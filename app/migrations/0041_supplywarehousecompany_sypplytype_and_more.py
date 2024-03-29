# Generated by Django 4.1.4 on 2023-04-20 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_alter_profile_moysklad_counterparty_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplyWarehouseCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Наименование компании')),
            ],
            options={
                'verbose_name': 'Компания (поставка)',
                'verbose_name_plural': 'Компании (поставка)',
                'db_table': 'app_supply_warehouse_company',
            },
        ),
        migrations.CreateModel(
            name='SypplyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Тип поставки')),
            ],
            options={
                'verbose_name': 'Тип поставки',
                'verbose_name_plural': 'Типы поставки',
                'db_table': 'app_supply_type',
            },
        ),
        migrations.AlterModelOptions(
            name='customadminpage',
            options={'verbose_name': 'Custom Admin Page', 'verbose_name_plural': 'Custom Admin Page'},
        ),
        migrations.AlterModelTable(
            name='warehouse',
            table='app_warehouse',
        ),
        migrations.CreateModel(
            name='SupplyWarehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Наименование склада')),
                ('address', models.CharField(max_length=500, verbose_name='Адрес склада')),
                ('opening_hours', models.CharField(blank=True, max_length=500, null=True, verbose_name='График работы склада')),
                ('how_to_get_there', models.TextField(blank=True, null=True, verbose_name='Как добраться до склада')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supply_warehouses_company', to='app.supplywarehousecompany', verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Склад (поставка)',
                'verbose_name_plural': 'Склады (поставка)',
                'db_table': 'app_supply_warehouse',
            },
        ),
        migrations.CreateModel(
            name='SupplyOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('order_number', models.IntegerField(verbose_name='Номер заказа')),
                ('customer_comment', models.TextField(blank=True, null=True, verbose_name='Комментарий клиента')),
                ('recipient_address', models.CharField(max_length=500, verbose_name='Адрес получателя')),
                ('recipient_full_name', models.CharField(max_length=500, verbose_name='ФИО получателя')),
                ('recipient_phone_number', models.CharField(max_length=500, verbose_name='Номер телефона получателя')),
                ('supply_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supply_type', to='app.sypplytype', verbose_name='Тип поставки')),
                ('supply_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supply_warehouse', to='app.supplywarehouse', verbose_name='Склад')),
            ],
            options={
                'verbose_name': 'Заказ на постаку',
                'verbose_name_plural': 'Заказы на поставку',
                'db_table': 'app_supply_order',
            },
        ),
    ]
