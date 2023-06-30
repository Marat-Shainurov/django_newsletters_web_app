from django.conf import settings
from django.core.cache import cache

from users.models import User


def get_cached_users_for_list_table():

    if settings.CACHE_ENABLED:
        key = 'users_list'
        users_list = cache.get(key)
        if users_list is None:
            users_list = User.objects.order_by('pk')
            cache.set(key, users_list)
            print('Cached users list is used')
    else:
        users_list = User.objects.order_by('pk')

    return users_list