from django.shortcuts import render, redirect
from django.contrib import messages
import base64

from datetime import datetime, time, date, timedelta

from .models import DateTimeSettings, Marketplace, Warehouse, PickupPoint, Page

from .decorators import group_required
from .tasks import make_handling_task

from app.excel_file_handling.utils import send_order_statuses_request, handling_order_statuses_request


@group_required('Клиенты')
def index(request):
    page = Page.objects.get(handler='index')
    return render(request, 'index.html', {"page": page})


@group_required('Клиенты')
def excel_upload(request):
    page = Page.objects.get(handler='excel_upload')
    return render(request, 'excel_upload.html', {"page": page})


@group_required('Клиенты')
def handling(request):
    # получаем список выходных дней и интервал времени загрузки
    date_time_settings = DateTimeSettings.objects.get(name="Загрузка файла").obj
    holidays = date_time_settings["holidays"]
    start_time = time(**date_time_settings["start_time"])
    end_time = time(**date_time_settings["end_time"])
    error_text = date_time_settings["error_text"]


    # получаем текущие дату, время и день недели
    now = datetime.now().replace(microsecond=0)
    date_now = now.date()
    time_now = now.time()
    weekday = date_now.isoweekday()

    # правило для загрузки
    if end_time > time_now > start_time and weekday not in holidays:
        file = request.FILES['file']
        # кодируем файл в строку для json сериализации в celery
        excel_raw_bytes = file.read()
        file_base64 = base64.b64encode(excel_raw_bytes).decode()

        make_handling_task.delay(request.user.id, file_base64, file.name)

        messages.add_message(request, messages.SUCCESS, 'Файл успешно загружен')
    else:
        messages.add_message(request, messages.ERROR, error_text)
    return redirect('excel_upload')


@group_required('Клиенты')
def pickup_point_list(request):
    page = Page.objects.get(handler='pickup_point_list')
    marketplaces = Marketplace.objects.all()
    return render(request, 'pickup_point_list.html', {"page": page, "marketplaces": marketplaces})


@group_required('Клиенты')
def order_statuses(request):
    page = Page.objects.get(handler='order_statuses')
    return render(request, 'order_statuses.html', {"page": page})


@group_required('Клиенты')
def supply(request):
    page = Page.objects.get(handler='supply')
    return render(request, 'supply.html', {"page": page})

from django.views.generic import TemplateView


@group_required('Клиенты')
def order_statuses_table(request):
    extra = request.user.profile.xml_api_extra
    login = request.user.profile.xml_api_login
    password = request.user.profile.xml_api_password

    max_date = date.today()
    min_date = max_date - timedelta(days=58)

    if request.method == "POST":
        datefrom = date(*[int(i) for i in request.POST.get("datefrom").split("-")])
        dateto = date(*[int(i) for i in request.POST.get("dateto").split("-")])
    else:
        dateto = date.today()
        datefrom = dateto - timedelta(days=3)

    # отправляем запрос на API сервиса
    response = send_order_statuses_request(extra, login, password, datefrom, dateto)

    # парсим запрос
    orders = handling_order_statuses_request(response)

    return render(request, 'order_statuses_table.html', {"orders": orders,
                                                         "datefrom": datefrom.strftime("%Y-%m-%d"),
                                                         "dateto": dateto.strftime("%Y-%m-%d"),
                                                         "max_date": max_date.strftime("%Y-%m-%d"),
                                                         "min_date": min_date.strftime("%Y-%m-%d")})





