from django.shortcuts import render, redirect
from landing.models import NavbarItem, Page, Service, Advantage
from app.excel_file_handling.notifications.e_mail import EmailNotification
from django.contrib import messages

# Create your views here.
def index(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        phone = request.POST.get("phone", "")
        messages.add_message(request, messages.SUCCESS, 'Заявка успешно отправлена')
        EmailNotification().culculation_request(name, phone)
        return redirect("/#lp-dl-count")
    else:
        navbar_items = NavbarItem.objects.all()
        page =  Page.objects.get(pk=1)
        services = Service.objects.all()
        advantages = Advantage.objects.all()
        return render(request, 'index.html', {"navbar_items": navbar_items,
                                              "page": page,
                                              "services": services,
                                              "advantages": advantages})

