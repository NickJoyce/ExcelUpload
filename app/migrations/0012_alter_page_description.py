# Generated by Django 4.1.4 on 2023-01-30 13:01

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_page_body_page_description_page_header_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]
