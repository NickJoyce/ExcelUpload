# Generated by Django 4.1.4 on 2023-01-30 09:24

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_page'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'verbose_name': 'Страница', 'verbose_name_plural': 'Страницы'},
        ),
        migrations.AlterField(
            model_name='page',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=None),
            preserve_default=False,
        ),
    ]
