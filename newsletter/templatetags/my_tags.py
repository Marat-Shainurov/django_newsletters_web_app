from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def media_path(file_name):
    media_url = settings.MEDIA_URL
    return f'{media_url}{file_name}'
