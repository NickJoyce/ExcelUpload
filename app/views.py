from django.shortcuts import render, redirect
from django.contrib import messages
import base64

from datetime import datetime, time, date, timedelta

from .models import DateTimeSettings, Marketplace, Warehouse, PickupPoint, Page
from .utils import Day

from .decorators import group_required
from .tasks import make_handling_task

from app.excel_file_handling.utils import send_order_statuses_request, handling_order_statuses_request
from app.excel_file_handling.utils import send_supply_order_request


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
        if request.method == "POST":
            extra = request.user.profile.xml_api_extra
            login = request.user.profile.xml_api_login
            password = request.user.profile.xml_api_password
            supply_date = request.POST.get("supply_date")
            d, m, y = supply_date.split(" ")[0].split(".")
            supply_date = f"{y}-{m}-{d}"
            marketplace_address = request.POST.get("marketplace_address")
            marketplace, address= marketplace_address.split(": ")
            send_supply_order_request(extra, login, password, supply_date, marketplace, address)
            messages.add_message(request, messages.SUCCESS, 'Заявка успешно отправлена')
            return redirect("supply")

        else:
            page = Page.objects.get(handler='supply')
            # получить дни недели когда возможны отгрузки [1-7] и сколько часов должно пройти от настоящего момента
            weekdays = [3, 6]
            # задержка (часы)
            time_delay = 36
            # определить текущую дату и время
            now = datetime.now().replace(microsecond=0)
            # получить день начиная с которого доступны поставки
            now_plus_time_delay = now + timedelta(hours=time_delay)
            datefrom = now_plus_time_delay.date()

            # сколько дней начиная с дня отгрузки доступны
            days_available_number = 60
            daysOftheWeek = ("ISO Week days start from 1",
                             "Понедельник",
                             "Вторник",
                             "Среда",
                             "Четверг",
                             "Пятница",
                             "Суббота",
                             "Воскресенье"
                             )
            # количнство дней в текущем месяце
            days = []
            for i in range(days_available_number):
                day = Day(date=datefrom.strftime("%d.%m.%Y"),
                          available_status=None,
                          day_of_the_week=daysOftheWeek[datefrom.isoweekday()])
                if datefrom.isoweekday() in weekdays:
                    day.available_status = True
                else:
                    day.available_status = False
                days.append(day)
                datefrom += timedelta(days=1)
            # получаем список маркетплейсов и связанные с ними склады
            marketplaces = Marketplace.objects.all()
            mp_list = []
            for marketplace in marketplaces:
                warehouses = Warehouse.objects.filter(marketplace=marketplace)
                for warehouse in warehouses:
                    mp_list.append(f"{marketplace.name}: {warehouse.address}")
            print(mp_list)
            return render(request, 'supply.html', {"page": page,
                                                   "now": now,
                                                   "datefrom": datefrom,
                                                   "days": days,
                                                   "mp_list": mp_list})


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

@group_required('Клиенты')
def supply_iframe_module(request):
    # получить дни недели когда возможны отгрузки [1-7] и сколько часов должно пройти от настоящего момента
    weekdays = [3, 6]
    # задержка (часы)
    time_delay = 36

    # определить текущую дату и время
    now = datetime.now().replace(microsecond=0)
    # получить день начиная с которого доступны поставки
    now_plus_time_delay = now + timedelta(hours=time_delay)
    datefrom = now_plus_time_delay.date()

    # сколько дней начиная с дня отгрузки доступны
    days_available_number = 60

    daysOftheWeek = ("ISO Week days start from 1",
                     "Понедельник",
                     "Вторник",
                     "Среда",
                     "Четверг",
                     "Пятница",
                     "Суббота",
                     "Воскресенье"
                     )

    # количнство дней в текущем месяце
    days = []
    for i in range(days_available_number):
        day = Day(date=datefrom.strftime("%d.%m.%Y"),
                  available_status=None,
                  day_of_the_week=daysOftheWeek[datefrom.isoweekday()])
        if datefrom.isoweekday() in weekdays:
            day.available_status = True
        else:
            day.available_status = False
        days.append(day)
        datefrom += timedelta(days=1)

    return render(request, 'supply_iframe_module.html', {"now": now,
                                                        "datefrom": datefrom,
                                                        "days": days})


