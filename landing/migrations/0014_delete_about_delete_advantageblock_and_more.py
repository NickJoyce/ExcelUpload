# Generated by Django 4.1.4 on 2023-06-18 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0013_alter_page_options_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='About',
        ),
        migrations.DeleteModel(
            name='AdvantageBlock',
        ),
        migrations.DeleteModel(
            name='ContactInfo',
        ),
        migrations.DeleteModel(
            name='CostCalculation',
        ),
        migrations.DeleteModel(
            name='Intro',
        ),
        migrations.DeleteModel(
            name='ServicesBlock',
        ),
    ]