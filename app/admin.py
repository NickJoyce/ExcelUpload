from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from .models import Profile, JsonObject, NotificationRecipients, DateTimeSettings
from .models import Marketplace, Warehouse, PickupPoint, Page, CustomPageModel
from django_json_widget.widgets import JSONEditorWidget
from app import views
from django.urls import path




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

@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    list_display = ['address', 'marketplace', 'opening_hours', 'how_to_get_there']
    list_filter = ['marketplace']

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['name', 'handler', 'html_file']
    fields = ['name', 'handler', 'html_file']




# Кастомная страница
@admin.register(CustomPageModel)
class CustomPageModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        view_name = f"{CustomPageModel._meta.app_label}_{CustomPageModel._meta.model_name}_changelist"
        return [
            path('upload_agreement/', views.upload_agreement, name=view_name)
        ]

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






