from django import template
from landing.models import General
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.simple_tag(name="general")
def get_general():
    try:
        return General.objects.get(pk=1)
    except ObjectDoesNotExist:
        return None

