# Generated by Django 4.1.4 on 2023-06-18 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0018_alter_page_copyright'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='copyright',
        ),
    ]
