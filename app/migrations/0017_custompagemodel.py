# Generated by Django 4.1.4 on 2023-02-06 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_profile_agreement'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Кастомные страницы',
            },
        ),
    ]
