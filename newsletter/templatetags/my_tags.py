from django import template
from django.conf import settings

from users.models import User

register = template.Library()


@register.simple_tag
def media_path(file_name):
    media_url = settings.MEDIA_URL
    return f'{media_url}{file_name}'


from django.contrib.auth.models import Group


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
