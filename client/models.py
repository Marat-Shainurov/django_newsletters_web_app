from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='client_name', unique=True)
    email = models.EmailField(max_length=50, verbose_name='client_email', unique=True)
    is_signed_up = models.BooleanField(verbose_name='is_signed_up', default=True)
    comments = models.TextField(verbose_name='additional_info')

    def __str__(self):
        return f'{self.name} {self.email}'

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'
