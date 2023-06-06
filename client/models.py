from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='client_name', unique=True)
    email = models.EmailField(max_length=50, verbose_name='client_email', unique=True)
    slug = models.SlugField(verbose_name='slug', **NULLABLE)
    is_signed_up = models.BooleanField(verbose_name='is_signed_up', default=True)
    is_active = models.BooleanField(verbose_name='is_active', default=True)
    comments = models.TextField(verbose_name='additional_info')
    created = models.DateTimeField(verbose_name='created', auto_now_add=True)

    def __str__(self):
        return f'{self.name} {self.email}'

    def save(self, **kwargs):
        self.slug = slugify(unidecode(self.name))
        super().save(**kwargs)

    def delete(self, **kwargs):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'
