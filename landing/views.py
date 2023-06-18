from django.shortcuts import render
from landing.models import NavbarItem, Page, Service,  Advantage
# Create your views here.
def index(request):
    navbar_items = NavbarItem.objects.all()
    page =  Page.objects.get(pk=1)
    services = Service.objects.all()
    advantages = Advantage.objects.all()
    return render(request, 'index.html', {"navbar_items": navbar_items,
                                          "page": page,
                                          "services": services,
                                          "advantages": advantages})

