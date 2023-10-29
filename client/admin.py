from django.contrib import admin

from client.models import Client, City


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'city', 'created', 'is_active', 'is_signed_up')
    list_filter = ('city', 'is_active', 'is_signed_up',)
    search_fields = ('name', 'email', 'comments',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('city',)
