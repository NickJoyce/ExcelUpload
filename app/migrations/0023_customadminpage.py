# Generated by Django 4.1.4 on 2023-02-11 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_profile_is_added_to_main_system'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomAdminPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Загрузка договора-оферты',
                'verbose_name_plural': 'Загрузка договора-оферты',
            },
        ),
    ]
