# Generated by Django 4.1.4 on 2023-04-26 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_alter_companysettings_warehouse'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companysettings',
            options={'verbose_name': 'Информация о компании', 'verbose_name_plural': 'Информация о компании'},
        ),
        migrations.RemoveField(
            model_name='companysettings',
            name='warehouse',
        ),
        migrations.AlterField(
            model_name='companysettings',
            name='name',
            field=models.CharField(default='ИП Иванов Иван Иванович', max_length=255, verbose_name='Наименование компании'),
        ),
        migrations.CreateModel(
            name='CompanyWarehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Наименование склада')),
                ('address', models.CharField(max_length=100, unique=True, verbose_name='Адрес склада')),
                ('opening_hours', models.CharField(blank=True, max_length=500, null=True, verbose_name='График работы склада')),
                ('how_to_get_there', models.TextField(blank=True, null=True, verbose_name='Как добраться до склада')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_warehouse', to='app.companysettings', verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Склад',
                'verbose_name_plural': 'Склады',
                'db_table': 'app_company_warehouse',
            },
        ),
    ]
