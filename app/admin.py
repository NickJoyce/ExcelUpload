from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from .models import Profile, JsonObject, NotificationRecipients, DateTimeSettings
from .models import Marketplace, Warehouse, PickupPoint, Page, CustomAdminPage
from django_json_widget.widgets import JSONEditorWidget
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from app import views
from project.settings.base import BASE_DIR
from django import apps
import os
from django.shortcuts import redirect
from .utils import File
from django.core.files.storage import FileSystemStorage
from django.contrib import messages




class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

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


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'marketplace', 'opening_hours', 'how_to_get_there']
    list_filter = ['marketplace']
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget}
    }



@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    list_display = ['address', 'marketplace', 'opening_hours', 'how_to_get_there']
    list_filter = ['marketplace']

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['name', 'handler', 'html_file']



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
                      file_path=f"{BASE_DIR}/app/static/pdf/agreement",
                      form_name="agreement",
                      input_accept="application/pdf"),
                File(th="Загрузка списка ПВЗ (.xls, .xlsx)",
                      file_path=f"{BASE_DIR}/app/static/excel/pickup_points",
                      form_name="pickup_points",
                      input_accept=".xls,.xlsx, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel")
                 ]
        if request.method == "POST":
            file = request.FILES['file']
            form_name = request.POST.get('form_name')
            for file_ in files:
                if file_.form_name == form_name:
                    # Очистить директорию agreement если она не пуста
                    dir = file_.file_path
                    for f in os.listdir(dir):
                        os.remove(os.path.join(dir, f))
                    # Загрузить файл в директорию
                    fs = FileSystemStorage(location=dir)
                    filename = fs.save(file.name, file)
                    break
            if form_name == "pickup_points":
                self.pickup_points_file_dandling(request, file)

            return redirect("admin:files_upload")
        else:
            data = dict(title="Загрузка файлов")
            data["files"] = files
            data = {**data, **self.admin_site.each_context(request)}
            return TemplateResponse(request, "admin/files_upload.html", data)

    def pickup_points_file_dandling(self, request, file):
        messages.add_message(request, messages.ERROR, 'Файл успешно загружен но нужна обработка')

























# class MyAdminSite(admin.AdminSite):
#     def get_app_list(self, request):
#         apps = [{"name": "appgg",
#                 "models":[
#                  {"name:": "link", "perms": {"change": True}, "admin_url": "https://web.telegram.org/z/#520704135"}
#                 ]
#                  }]
#         return apps + super().get_app_list(request)
#
# my_site = MyAdminSite(name="my_site")

#
#     def get_app_list(self, request):
#         apps = [{'name': 'Apps',
#                 "models":[
#                  {'name': 'Загрузка договора-оферты2', 'perms': {'add': True, 'change': True, 'delete': True, 'view': True}, 'admin_url': '/admin/app/custompagemodel/'}
#                 ]
#                  }]
#         return apps + self.admin_site.get_app_list(request)


















admin.site.site_title = "Администрирование account.zvwb.ru"
admin.site.site_header = "Администрирование account.zvwb.ru"


# class MyAdminSite(admin.AdminSite):
#     def get_app_list(self, request):
#         apps = [{"name": "app",
#                 "models":[
#                  {"name:": "link", "perms": {"change": True}, "admin_url": "https://web.telegram.org/z/#520704135"}
#                 ]
#                  }]
#         return apps + super(MyAdminSite, self).get_app_list(request)


# from django.urls import path
# from django.contrib import admin
# from django.http import HttpResponse
#
# class CustomAdminSite(admin.AdminSite):
#
#     def my_view(self, request):
#         return HttpResponse("Hello!")
#
#     def get_urls(self):
#         urls = super(CustomAdminSite, self).get_urls()
#         custom_urls = [
#             path('testpath', self.admin_view(self.my_view), name="testview"),
#         ]
#         return custom_urls + urls
#
#
# class TemplateAdmin(admin.ModelAdmin):
#     ...
#     change_form_template = 'admin/test.html'


