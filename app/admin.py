from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from .models import Profile, JsonObject, NotificationRecipients, DateTimeSettings
from .models import Marketplace, Warehouse, PickupPoint, Page, CustomAdminPage
from .models import SupplyWarehouseCompany, SupplyWarehouse, SypplyType, SupplyOrder
from django_json_widget.widgets import JSONEditorWidget
from django.template.response import TemplateResponse
from django.urls import path
import os
from django.shortcuts import redirect
from .utils import File, pickup_points_file_handling
from django.core.files.storage import FileSystemStorage
from project.settings.base import FILE_LOCATIONS
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    ordering = ['company']
    fieldsets = (
        (None, {
            'fields': ('phone', 'company', 'inn'),
        }),
        ('Вход в сиcтему', {
            'fields': ('xml_api_extra', 'xml_api_login', 'xml_api_password'),
        }),
        ('Прочее', {
            'fields': ('agreement', 'personal_data_agreement', 'is_added_to_main_system', 'moysklad_counterparty_id'),
        }),
    )



class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_select_related = ('profile',)
    list_display = ["username", "email", "first_name", "last_name", "get_company", "get_id_moysklad", "get_is_added_to_main_system"]
    list_filter = ["profile__is_added_to_main_system"]


    fieldsets = (
        (_('Permissions'), {'classes': ('collapse',),
                            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),}),
        (_('Important dates'), {'classes': ('collapse',),
                                'fields': ('last_login', 'date_joined')}),
        ('Регистрационные данные', {'classes': ('collapse',),
                                    'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),}),)



    @admin.display(description='ЛК акт.?', ordering="profile__is_added_to_main_system")
    def get_is_added_to_main_system(self, obj) -> str:
        if obj.profile.is_added_to_main_system:
            return format_html(
                f"<img src='/static/admin/img/icon-yes.svg' alt='True'>"
            )
        elif obj.profile.is_added_to_main_system == False:
            return format_html(
                f"<img src='/static/admin/img/icon-no.svg' alt='False'>"
            )
        else:
            return "-"


    @admin.display(description='Компания', ordering="profile__company")
    def get_company(self, obj) -> str:
            return obj.profile.company

    @admin.display(description='id в Мой склад', ordering="profile__moysklad_counterparty_id")
    def get_id_moysklad(self, obj) -> str:
            return obj.profile.moysklad_counterparty_id


    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)



@admin.register(JsonObject)
class JsonObjectAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget}
    }


@admin.register(NotificationRecipients)
class NotificationRecipientsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'telegram_id', 'is_active']


@admin.register(DateTimeSettings)
class DateTimeSettingsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget}
    }


@admin.register(Marketplace)
class MarketplaceAdmin(admin.ModelAdmin):
    list_display = ['name']



@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    list_display = ['address', 'marketplace', 'opening_hours', 'how_to_get_there']
    list_filter = ['marketplace']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    fields = ['name', 'is_active', 'sorting_order', 'title', 'header', 'description']
    list_display = ['name', 'is_active', 'sorting_order']


@admin.register(CustomAdminPage)
class CustomAdminPageAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('files_upload/', self.admin_site.admin_view(self.files_upload), name="files_upload"),
        ]
        return my_urls + urls

    def files_upload(self, request):
        files = [
                File(th="Загрузка договора-оферты (.pdf)",
                      file_path=FILE_LOCATIONS["agreement"],
                      form_ident="agreement",
                      input_accept="application/pdf"),
                File(th="Загрузка списка ПВЗ (.xls, .xlsx)",
                      file_path=FILE_LOCATIONS["pickup_points"],
                      form_ident="pickup_points",
                      input_accept=".xls,.xlsx, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel"),
                File(th="Загрузка Соглашения об обработке персональных данных (.pdf)",
                     file_path=FILE_LOCATIONS["personal_data_agreement"],
                     form_ident="personal_data_agreement",
                     input_accept="application/pdf")
                 ]
        if request.method == "POST":
            file = request.FILES['file']
            form_ident = request.POST.get('form_ident')
            for file_item in files:
                if file_item.form_ident == form_ident:
                    # Очистить директорию agreement если она не пуста
                    for f in os.listdir(file_item.file_path):
                        os.remove(os.path.join(file_item.file_path, f))
                    # Загрузить файл в директорию
                    fs = FileSystemStorage(location=file_item.file_path)
                    fs.save(file.name, file)
                    break
            if form_ident == "pickup_points":
                pickup_points_file_handling(request, file)

            return redirect("admin:files_upload")
        else:
            data = dict(title="Загрузка файлов")
            data["files"] = files
            data = {**data, **self.admin_site.each_context(request)}
            return TemplateResponse(request, "admin/files_upload.html", data)

admin.site.site_title = "Администрирование account.zvwb.ru"
admin.site.site_header = "Администрирование account.zvwb.ru"








# @admin.register(Warehouse)
# class WarehouseAdmin(admin.ModelAdmin):
#     list_display = ['name', 'address', 'marketplace', 'opening_hours', 'how_to_get_there']
#     list_filter = ['marketplace']
#     formfield_overrides = {
#         models.JSONField: {'widget': JSONEditorWidget}
#     }


# @admin.register(SupplyWarehouseCompany)
# class SupplyWarehouseCompanyAdmin(admin.ModelAdmin):
#     list_display = ['name']
#
# @admin.register(SupplyWarehouse)
# class SupplyWarehouseAdmin(admin.ModelAdmin):
#     list_display = ['name', 'company', 'address',  'opening_hours', 'how_to_get_there']
#     list_filter = ['company']
#
# @admin.register(SypplyType)
# class SypplyTypeAdmin(admin.ModelAdmin):
#     list_display = ['name']
#
# @admin.register(SupplyOrder)
# class SupplyOrderAdmin(admin.ModelAdmin):
#     list_display = ['order_number', 'supply_type', 'supply_warehouse', 'created']
#     list_filter = ['supply_type', 'supply_warehouse']