from django.contrib import admin
from landing.models import NavbarItem, Page, Service, Advantage, General

# Register your models here.
@admin.register(NavbarItem)
class NavbarItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'href', 'is_account', 'is_active', 'sorting_order']

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Введение', {
            'fields': ('intro_header', 'intro_text', 'intro_image',),
        }),
        ('О компании', {
            'fields': ('about_header', 'about_text',),
        }),
        ('Услуги', {
            'fields': ('service_header',),
        }),
        ('Преимущества', {
            'fields': ('advantage_header',),
        }),

        ('Расчет стоимости', {
            'fields': ('cost_calculation_header', 'cost_calculation_text', 'cost_calculation_privacy_policy',
                       'cost_calculation_image',),
        }),

        ('Контакты', {
            'fields': ('contact_header', 'contact_yandex_iframe_src',),
        })
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['header', 'sorting_order']


@admin.register(Advantage)
class AdvantageAdmin(admin.ModelAdmin):
    list_display = ['header', 'sorting_order']

@admin.register(General)
class GeneralAdmin(admin.ModelAdmin):
    ...