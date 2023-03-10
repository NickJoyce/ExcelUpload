# Generated by Django 4.1.4 on 2023-01-17 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_notificationrecipients'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateTimeSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Имя')),
                ('obj', models.JSONField(verbose_name='Настрока дат и времени')),
            ],
            options={
                'verbose_name': 'Настрока дат и времени',
                'verbose_name_plural': 'Настроки дат и времени',
            },
        ),
        migrations.AlterModelOptions(
            name='jsonobject',
            options={'verbose_name': 'Настрока вариаций наименования', 'verbose_name_plural': 'Настрока вариаций наименования'},
        ),
    ]
