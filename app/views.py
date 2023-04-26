from django.shortcuts import render as base_render
from django.shortcuts import redirect
from django.contrib import messages
import base64
import json
from django.http import FileResponse
from datetime import datetime, time, date, timedelta
from .models import DateTimeSettings, Page, Marketplace, CompanyWarehouse
from .utils import File
from .moysklad.utils import SaleChannel, is_counterparty, create_order
from .decorators import group_required
from .tasks import make_handling_task, send_order_to_moysklad_task
from app.excel_file_handling.utils import send_order_statuses_request, handling_order_statuses_request
from app.excel_file_handling.utils import send_supply_order_request
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth.models import Group
import os
from project.settings.base import FILE_LOCATIONS, MOYSKLAD_TOKEN, MOYSKLAD_ORGANIZATION_ID
from app.excel_file_handling.notifications.telegram import send_signup_telegram_notification
from app.excel_file_handling.notifications.telegram import send_supply_telegram_notification

from project.settings.base import MOYSKLAD_TOKEN
import requests





def render(request, template_name, context):
    context["pages"] = Page.objects.all()
    return base_render(request, template_name, context)


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
    return render(request, 'pickup_point_list.html', {"page": page,
                                                      "marketplaces": marketplaces})


@group_required('Клиенты')
def order_statuses(request):
    page = Page.objects.get(handler='order_statuses')
    return render(request, 'order_statuses.html', {"page": page})


@group_required('Клиенты')
def supply(request):
    if request.method == "POST":
        sales_channel_id = request.POST.get("sales_channel", "")
        comment = request.POST.get("comment", "")
        recipient_address = request.POST.get("address", "")
        recipient_full_name = request.POST.get("full_name", "")
        recipient_phone = request.POST.get("phone", "")

        counterparty_id = request.user.profile.moysklad_counterparty_id
        user_id = request.user.id

        send_order_to_moysklad_task.delay(user_id = user_id,
                                          sales_channel_id=sales_channel_id,
                                          comment=comment,
                                          recipient_address=recipient_address,
                                          recipient_full_name=recipient_full_name,
                                          recipient_phone=recipient_phone,
                                          counterparty_id=counterparty_id)

        messages.add_message(request, messages.SUCCESS, 'Заказ успешно создан. Спасибо!')

        return redirect("supply")
    else:
        page = Page.objects.get(handler='supply')
        url = f"https://online.moysklad.ru/api/remap/1.2/entity/saleschannel"
        headers = {'Authorization': f'Bearer {MOYSKLAD_TOKEN}', 'Content-Type': 'application/json'}
        try:
            response = requests.get(url=url, headers=headers)
            sales_channels = [SaleChannel(row['id'], row['name'])  for row in response.json()['rows'] if row['name'] != "Проверка наличия / Пересчёт"]
        except:
            sales_channels = []

        try:
            warehouse = CompanyWarehouse.objects.all()[0]
        except IndexError:
            warehouse = None


        return render(request, 'supply.html', {"page": page,
                                               "sales_channels": sales_channels,
                                               "warehouse": warehouse})



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


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.company = form.cleaned_data.get('company')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.inn = form.cleaned_data.get('inn')
            user.profile.agreement = form.cleaned_data.get('agreement')
            user.profile.personal_data_agreement = form.cleaned_data.get('personal_data_agreement')
            user.profile.xml_api_extra = "26"
            user.profile.xml_api_login = form.cleaned_data.get('username')
            user.profile.xml_api_password = form.cleaned_data.get('password1')
            user.profile.is_added_to_main_system = False
            group = Group.objects.get(name="Клиенты")
            user.groups.add(group)
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            send_signup_telegram_notification(username=user.username,
                                              company=user.profile.company,
                                              first_name=user.first_name,
                                              last_name=user.last_name,
                                              phone=user.profile.phone,
                                              email=user.email)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def download_file(request, file_type):
    # директория где лежит загружаемый файл
    file_path = FILE_LOCATIONS[file_type]
    # имя загружаемого файла
    filename = File.get_file_name(file_path)
    if filename == "---файл не загружен---":
        messages.add_message(request, messages.ERROR, filename)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return FileResponse(open(os.path.join(file_path, filename), 'rb'))

