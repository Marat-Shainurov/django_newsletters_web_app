from django.conf import settings
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

from client.models import Client,City
from newsletter.models.schedule import Schedule

NULLABLE = {'blank': True, 'null': True}


class Newsletter(models.Model):
    STATUS_CHOICE = [
        ('created', 'Created'),
        ('launched', 'Launched'),
        ('finished', 'Finished'),
    ]

    newsletter = models.CharField(max_length=100, verbose_name='newsletter_title')
    slug = models.SlugField(max_length=250, verbose_name='slug', **NULLABLE)
    start_campaign = models.DateTimeField(verbose_name='from')
    finish_campaign = models.DateTimeField(verbose_name='until')
    status = models.CharField(max_length=10, default='created', choices=STATUS_CHOICE, verbose_name='newsletter_status')
    regularity = models.ForeignKey(Schedule, verbose_name='regularity_settings', on_delete=models.SET_NULL, **NULLABLE)
    subject = models.CharField(max_length=100, verbose_name='subject', unique=True)
    content = models.TextField(verbose_name='content')
    is_active = models.BooleanField(verbose_name='is_active', default=True)
    created = models.DateTimeField(verbose_name='created', auto_now_add=True)

    newsletter_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='newsletter_user',
                                        on_delete=models.CASCADE, **NULLABLE)
    newsletter_clients = models.ManyToManyField(Client, related_name='client_newsletters')
    newsletter_cities = models.ManyToManyField(City, related_name='city_newsletters')

    def __str__(self):
        return f'{self.newsletter} {self.pk} / {self.status} / {self.regularity}'

    def save(self, *args, **kwargs):
        if self.slug:
            super().save(*args, **kwargs)
        else:
            self.slug = slugify(unidecode(self.subject))
            super().save(*args, **kwargs)

    def delete(self, **kwargs):
        self.is_active = False
        super().delete(**kwargs)
        self.save()

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'
        permissions = [
            (
                'remove_regular_newsletter',
                'can remove regular newsletter'
            )
        ]
