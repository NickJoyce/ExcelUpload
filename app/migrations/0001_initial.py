# Generated by Django 4.1.4 on 2022-12-28 12:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(blank=True, max_length=30, verbose_name='Компания')),
                ('phone', models.CharField(blank=True, max_length=30, verbose_name='Телефон')),
                ('xml_api_extra', models.CharField(max_length=30, verbose_name='Экстра-код')),
                ('xml_api_login', models.CharField(max_length=30, verbose_name='Логин клиента')),
                ('xml_api_password', models.CharField(max_length=30, verbose_name='Пароль клиента')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
