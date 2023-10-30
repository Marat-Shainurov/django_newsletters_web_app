from django.conf import settings
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

NULLABLE = {'blank': True, 'null': True}


class City(models.Model):
    city = models.CharField(verbose_name='city_name', max_length=50, unique=True)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.city


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='client_name', unique=True)
    email = models.EmailField(max_length=50, verbose_name='client_email', unique=True)
    slug = models.SlugField(verbose_name='slug', **NULLABLE)
    is_signed_up = models.BooleanField(verbose_name='is_signed_up', default=True)
    is_active = models.BooleanField(verbose_name='is_active', default=True)
    comments = models.TextField(verbose_name='additional_info', **NULLABLE)
    created = models.DateTimeField(verbose_name='created', auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='user_clients', **NULLABLE)
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, related_name='city_clients', verbose_name='client_city', **NULLABLE)

    def __str__(self):
        return f'{self.name} {self.email}'

    def save(self, *args, **kwargs):
        if self.slug:
            super().save(*args, **kwargs)
        else:
            self.slug = slugify(unidecode(self.name))
            super().save(**kwargs)

    def delete(self, **kwargs):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'
