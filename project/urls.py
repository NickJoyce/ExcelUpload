"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from app import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test
from project.settings.base import BASE_DIR


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  views.index, name='index'),
    path('pickup_point_list/',  views.pickup_point_list, name='pickup_point_list'),
    path('order_statuses/',  views.order_statuses, name='order_statuses'),
    path('supply/',  views.supply, name='supply'),
    path('excel_upload/',  views.excel_upload, name='excel_upload'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('order_statuses_table/',  views.order_statuses_table, name='order_statuses_table'),
    # path('supply_iframe_module/', views.supply_iframe_module, name='supply_iframe_module'),
    path('signup/', views.signup, name='signup'),
    path('handling/',  views.handling, name='handling'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls'))
]

urlpatterns += [
    path('download-file/<str:file_type>', views.download_file, name='download_file')
]

