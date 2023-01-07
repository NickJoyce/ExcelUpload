from django.shortcuts import render, redirect
from django.contrib import messages
import base64

from .decorators import group_required
from .tasks import make_handling_task


@group_required('Клиенты')
def index(request):
    return render(request, 'index.html')


@group_required('Клиенты')
def handling(request):
    file = request.FILES['file']
    # кодируем файл в строку для json сериализации в celery
    excel_raw_bytes = file.read()
    file_base64 = base64.b64encode(excel_raw_bytes).decode()

    make_handling_task.delay(request.user.id, file_base64, file.name)

    messages.add_message(request, messages.SUCCESS, 'Файл успешно загружен')
    return redirect('index')

