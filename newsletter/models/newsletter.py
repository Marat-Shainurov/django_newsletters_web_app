from django.conf import settings
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

NULLABLE = {'blank': True, 'null': True}


class Newsletter(models.Model):
    STATUS_CHOICE = [
        ('created', 'Created'),
        ('launched', 'Launched'),
        ('finished', 'Finished'),
    ]

    REGULARITY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    newsletter = models.CharField(max_length=100, verbose_name='newsletter_name')
    slug = models.SlugField(max_length=250, verbose_name='slug', **NULLABLE)
    start_campaign = models.DateTimeField(verbose_name='from')
    finish_campaign = models.DateTimeField(verbose_name='until')
    status = models.CharField(max_length=10, default='created', choices=STATUS_CHOICE, verbose_name='newsletter_status')
    regularity = models.CharField(max_length=10, choices=REGULARITY_CHOICES, verbose_name='newsletter_regularity')
    subject = models.CharField(max_length=100, verbose_name='subject', unique=True)
    content = models.TextField(verbose_name='content')
    is_active = models.BooleanField(verbose_name='is_active', default=True)
    created = models.DateTimeField(verbose_name='created', auto_now_add=True)

    newsletter_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='newsletter_user',
                                        on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.newsletter} (pk - {self.pk}, {self.status}, {self.regularity})'

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
