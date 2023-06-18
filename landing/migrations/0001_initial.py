# Generated by Django 4.1.4 on 2023-06-18 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Navbar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Пункт меню')),
                ('href', models.CharField(max_length=1000, verbose_name='Ссылка')),
                ('is_account', models.BooleanField(default=False, verbose_name='Ссылка на личный кабинет?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Показ в меню')),
                ('sorting_order', models.IntegerField(default=1, verbose_name='Порядок сортировки')),
            ],
            options={
                'verbose_name': 'Пункт меню',
                'verbose_name_plural': 'Пункты меню',
            },
        ),
    ]
