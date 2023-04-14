# Generated by Django 4.1.4 on 2023-04-14 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_alter_profile_moysklad_counterparty_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='moysklad_counterparty_id',
            field=models.CharField(default='Контрагент не добавлен в Мой Склад!', help_text='чтобы добавить контрагента: [ЛК активирован: да] + [данное поле должно быть пустым]', max_length=255, verbose_name='id контрагента в МойСклад'),
        ),
    ]
