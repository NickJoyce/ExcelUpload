from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=30, blank=True, verbose_name="Компания")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Телефон")
    xml_api_extra = models.CharField(max_length=30, verbose_name="Экстра-код")
    xml_api_login = models.CharField(max_length=30, verbose_name="Логин клиента")
    xml_api_password = models.CharField(max_length=30, verbose_name="Пароль клиента")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

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
