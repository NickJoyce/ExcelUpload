# Generated by Django 4.1.4 on 2023-02-04 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_profile_agreement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='agreement',
            field=models.BooleanField(default=False, verbose_name='Согласие'),
        ),
    ]