from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from ckeditor_uploader.fields import RichTextUploadingField
from project.settings.base import MOYSKLAD_TOKEN
import requests
import base64
import json



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company = models.CharField(max_length=30, null=True, blank=True, verbose_name="Компания")
    phone = models.CharField(max_length=30, null=True, blank=True,  verbose_name="Телефон")
    inn = models.CharField(max_length=30, null=True, blank=True,  verbose_name="ИНН")
    xml_api_extra = models.CharField(max_length=30, verbose_name="Экстра-код")
    xml_api_login = models.CharField(max_length=30, verbose_name="Логин клиента")
    xml_api_password = models.CharField(max_length=30, verbose_name="Пароль клиента")
    agreement = models.BooleanField(default=False, verbose_name="Принятие договора-оферты")
    personal_data_agreement = models.BooleanField(default=False, verbose_name="Согласие на обработку персональных данных")
    is_added_to_main_system = models.BooleanField(default=False, verbose_name="ЛК активирован?")
    moysklad_counterparty_id = models.CharField(max_length=255, default="Контрагент не добавлен в Мой Склад!", null=True, blank=True,
                                                   verbose_name="id контрагента в МойСклад",
                                                    help_text="чтобы добавить контрагента: [ЛК активирован: да] + [данное поле должно быть пустым]")


    def save(self, *args, **kwargs):
        if self.is_added_to_main_system and not self.moysklad_counterparty_id:
            url = "https://online.moysklad.ru/api/remap/1.2/entity/counterparty"
            headers = {'Authorization': f'Bearer {MOYSKLAD_TOKEN}', 'Content-Type': 'application/json'}
            data = {"legalFirstName": "Иван",
                    "legalLastName": "Иванов",
                    "email": "raduga@stroi.ru",
                    "phone": "+74953312233",
                    "name": "TEST",
                    "inn": "125152124152"}
            response = requests.post(url=url, headers=headers, data=json.dumps(data))
            self.moysklad_counterparty_id = response.json()['id']
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        pass


class JsonObject(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Имя")
    obj = models.JSONField(verbose_name="JSON объект")

    class Meta:
        verbose_name = "Настрока вариаций наименования"
        verbose_name_plural = "Настрока вариаций наименования"

    def __str__(self):
        return f"{self.name}"

class NotificationRecipients(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(null=True, blank=True, verbose_name="Email")
    telegram_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="Телеграм id")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Получатель уведомлений"
        verbose_name_plural = "Получатели уведомлений"

    def __str__(self):
        return f"{self.name}"


class DateTimeSettings(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Имя")
    obj = models.JSONField(verbose_name="Настрока дат и времени")

    class Meta:
        verbose_name = "Настрока дат и времени"
        verbose_name_plural = "Настроки дат и времени"

    def __str__(self):
        return f"{self.name}"


class Marketplace(models.Model):
    name = models.CharField(max_length=100,  unique=True, verbose_name="Наименование маркетплейса")


    class Meta:
        verbose_name = "Маркетплейс"
        verbose_name_plural = "Маркетплейсы"

    def __str__(self):
        return f"{self.name}"

class Warehouse(models.Model):
    marketplace = models.ForeignKey(Marketplace, verbose_name="Маркетплейс", on_delete=models.CASCADE,
                                    related_name='warehouses')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Наименование склада")
    address = models.CharField(max_length=100, unique=True, verbose_name="Адрес склада")
    opening_hours = models.CharField(max_length=500, null=True, blank=True, verbose_name="График работы склада")
    how_to_get_there = models.TextField(null=True, blank=True, verbose_name="Как добраться до склада")
    supply_dates = models.JSONField(verbose_name="Даты поставок", default=list, null=True, blank=True)



    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

    def __str__(self):
        return f"{self.name}"


class PickupPoint(models.Model):
    marketplace = models.ForeignKey(Marketplace, verbose_name="Маркетплейс", on_delete=models.CASCADE,
                                    related_name='pickup_points')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Наименование пункта выдачи")
    address = models.CharField(max_length=100, verbose_name="Адрес пункта выдачи")
    opening_hours = models.CharField(max_length=500, null=True, blank=True, verbose_name="График работы пункта выдачи")
    how_to_get_there =models.TextField(null=True, blank=True, verbose_name="Как добраться до пункта выдачи")

    def display_marketplace(self):
        return self.marketplace.name

    class Meta:
        verbose_name = "ПВЗ"
        verbose_name_plural = "ПВЗ"
        db_table = 'app_pickup_point'


    def __str__(self):
        return f"{self.address}"

class Page(models.Model):
    handler = models.CharField(max_length=200, verbose_name="Функция-обработчик = url")
    html_file = models.CharField(max_length=200, verbose_name="HTML файл")
    name = models.CharField(max_length=200, verbose_name="Имя (в меню)")
    title = models.CharField(max_length=200, verbose_name="Текст во вкладке браузера")
    header = models.CharField(max_length=200, null=True, blank=True, verbose_name="Заголовок страницы")
    description = RichTextUploadingField(null=True, blank=True, verbose_name="Описание")
    is_active = models.BooleanField(verbose_name="Показ в меню", default=True)
    sorting_order = models.IntegerField(verbose_name="Порядок сортировки", default=1)


    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ['sorting_order']


    def __str__(self):
        return f"{self.name}"


class CustomAdminPage(models.Model):
    class Meta:
        verbose_name = 'Хрень'
        verbose_name_plural = "Хрень"