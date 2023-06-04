from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='client_name')
    email = models.EmailField(max_length=50, verbose_name='client_email')
    is_signed_up = models.BooleanField(default=True)
    comments = models.TextField(verbose_name='additional_info')

    def __str__(self):
        return f'{self.name} {self.email}'

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'
