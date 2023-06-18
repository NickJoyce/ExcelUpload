from django.db import models
from app.models import SingletonModel
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class NavbarItem(models.Model):
    name = models.CharField(max_length=255, verbose_name="Пункт меню")
    href = models.CharField(max_length=1000, verbose_name="Ссылка")
    is_account = models.BooleanField(verbose_name="Ссылка на личный кабинет?", default=False)
    is_active = models.BooleanField(verbose_name="Показ в меню", default=True)
    sorting_order = models.IntegerField(verbose_name="Порядок сортировки", default=1)

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"
        ordering = ['sorting_order']

    def __str__(self):
        return f"{self.name}"


class Page(SingletonModel):
    # intro
    intro_header = RichTextUploadingField(null=True, blank=True, verbose_name="Заголовок")
    intro_text = RichTextUploadingField(null=True, blank=True, verbose_name="Текст")
    intro_image = models.ImageField(upload_to="intro_img/", verbose_name="Изображение")
    # about
    about_header = models.CharField(max_length=255, verbose_name="Заголовок")
    about_text = RichTextUploadingField(null=True, blank=True, verbose_name="Текст")
    # service
    service_header = models.CharField(max_length=255, verbose_name="Заголовок")
    # advantage
    advantage_header = models.CharField(max_length=255, verbose_name="Заголовок")
    # cost_calculation
    cost_calculation_header = RichTextUploadingField(max_length=255, verbose_name="Заголовок")
    cost_calculation_text = RichTextUploadingField(null=True, blank=True, verbose_name="Текст")
    cost_calculation_privacy_policy = RichTextUploadingField(null=True, blank=True, verbose_name="Политика конфиденциальности")
    cost_calculation_image = models.ImageField(upload_to="costcalc_img/", verbose_name="Изображение")
    # contact
    contact_header = models.CharField(max_length=255, verbose_name="Заголовок")
    contact_yandex_iframe_src = models.CharField(max_length=1000, verbose_name="Яндекс карта (iframe src)")

    def __str__(self):
        return f"Страница"

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"



class Service(models.Model):
    image = models.ImageField()
    header = models.CharField(max_length=255, verbose_name="Заголовок")
    text = RichTextUploadingField(null=True, blank=True, verbose_name="Текст")

    def __str__(self):
        return f"{self.header}"

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        db_table = 'landing_service'



class Advantage(models.Model):
    header = models.CharField(max_length=255, verbose_name="Заголовок")
    text = RichTextUploadingField(null=True, blank=True, verbose_name="Текст")
    sorting_order = models.IntegerField(verbose_name="Порядок сортировки", default=1)

    def __str__(self):
        return f"{self.header}"

    class Meta:
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"
        db_table = 'landing_advantage'
        ordering = ['sorting_order']

class General(SingletonModel):
    favicon = models.ImageField(upload_to="favicon/", verbose_name="Favicon")
    copyright = models.CharField(max_length=255, verbose_name="Копирайт в футере")

    def __str__(self):
        return "Прочее"

    class Meta:
        verbose_name = "Прочее"
        verbose_name_plural = "Прочее"
        db_table = 'landing_general'




