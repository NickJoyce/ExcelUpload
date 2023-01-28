from django.shortcuts import render, redirect
from django.contrib import messages
import base64

from datetime import datetime
from datetime import time

from .models import DateTimeSettings, Marketplace, Warehouse, PickupPoint

from .decorators import group_required
from .tasks import make_handling_task


@group_required('Клиенты')
def index(request):
    return render(request, 'index.html')


@group_required('Клиенты')
def excel_upload(request):
    return render(request, 'excel_upload.html')


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
    marketplaces = Marketplace.objects.all()
    return render(request, 'pickup_point_list.html', {"marketplaces": marketplaces})

@group_required('Клиенты')
def order_statuses(request):
    return render(request, 'order_statuses.html')

@group_required('Клиенты')
def supply(request):
    return render(request, 'supply.html')


