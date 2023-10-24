from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


def create_manager_group():
    group_name = "Manager"
    group = Group(name=group_name)
    group.save()
    group.permissions.add(
        Permission.objects.get(codename='block_user'),
        Permission.objects.get(codename='set_schedule'),
        Permission.objects.get(codename='remove_regular_newsletter'),
    )


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        create_manager_group()
