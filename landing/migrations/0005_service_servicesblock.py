# Generated by Django 4.1.4 on 2023-06-18 07:30

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0004_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('header', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Список услуг',
                'db_table': 'landing_service',
            },
        ),
        migrations.CreateModel(
            name='ServicesBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=255, verbose_name='Заголовок')),
            ],
            options={
                'verbose_name': 'Услуги',
                'verbose_name_plural': 'Услуги',
                'db_table': 'landing_services',
            },
        ),
    ]
