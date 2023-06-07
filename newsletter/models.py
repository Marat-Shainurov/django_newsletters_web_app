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

    def __str__(self):
        return f'{self.newsletter} ({self.status} {self.regularity})'

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.subject))
        super().save(*args, **kwargs)

    def delete(self, **kwargs):
        self.is_active = False
        super().delete(**kwargs)
        self.save()

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'


class NewsletterAttempts(models.Model):
    ATTEMPT_STATUS_CHOICES = [
        ('success', 'Success'),
        ('failure', 'Failure'),
        ('in_progress', 'In_progress'),
    ]

    newsletter = models.ForeignKey(Newsletter, verbose_name='newsletter', on_delete=models.CASCADE)
    last_attempt = models.DateTimeField(verbose_name='last_attempt', **NULLABLE)
    attempt_status = models.CharField(max_length=12, choices=ATTEMPT_STATUS_CHOICES, verbose_name='attempt_status',
                                      **NULLABLE)
    email_server_response = models.TextField(verbose_name='email_server_response', **NULLABLE)

    def __str__(self):
        return f'{self.newsletter} (last attempt - {self.last_attempt}, {self.attempt_status})'

    class Meta:
        verbose_name = 'Newsletter Attempt'
        verbose_name_plural = 'Newsletter Attempts'
