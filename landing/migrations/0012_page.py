# Generated by Django 4.1.4 on 2023-06-18 08:56

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0011_contactinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intro_header', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Интро заголовок')),
                ('intro_text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Интро текст')),
                ('intro_image', models.ImageField(upload_to='', verbose_name='Интро изображение')),
                ('about_header', models.CharField(max_length=255, verbose_name='Заголовок О компании')),
                ('about_text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Текст О компании')),
                ('service_header', models.CharField(max_length=255, verbose_name='Заголовок Услуги')),
                ('advantage_header', models.CharField(max_length=255, verbose_name='Заголовок Премущества')),
                ('cost_calculation_header', models.CharField(max_length=255, verbose_name='Заголовок Расчет стоимости')),
                ('cost_calculation_text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Текст Расчет стоимости')),
                ('cost_calculation_privacy_policy', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Политика конфиденциальности')),
                ('cost_calculation_image', models.ImageField(upload_to='', verbose_name='изображение Расчет стоимости')),
                ('contact_header', models.CharField(max_length=255, verbose_name='Заголовок Контакты')),
                ('contact_yandex_iframe_src', models.CharField(max_length=1000, verbose_name='Яндекс карта (iframe src)')),
                ('copyright', models.CharField(max_length=255, verbose_name='Копирайт в футере')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
