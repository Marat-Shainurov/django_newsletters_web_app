from django.db import models

NULLABLE = {'blank': True, 'null': True}


class NewsletterSettings(models.Model):
    STATUS_CHOICE = [
        ('created', 'Created'),
        ('launched', 'Launched'),
        ('finished', 'Finished'),
    ]

    REGULARITY_CHOICES = [
        ('daily', 'Daily'),
        ('daily', 'Weekly'),
        ('daily', 'Monthly'),
    ]

    newsletter = models.CharField(max_length=100, verbose_name='newsletter_name')
    start_campaign = models.DateTimeField(verbose_name='from')
    finish_campaign = models.DateTimeField(verbose_name='until')
    status = models.CharField(max_length=10, default='created', choices=STATUS_CHOICE, verbose_name='newsletter_status')
    regularity = models.CharField(max_length=10, choices=REGULARITY_CHOICES, verbose_name='newsletter_regularity')

    def __str__(self):
        return f'{self.newsletter} ({self.status} {self.regularity})'

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'


class NewsletterAttempts(models.Model):
    ATTEMPT_STATUS_CHOICES = [
        ('success', 'Success'),
        ('failure', 'Failure'),
        ('in_progress', 'In_progress'),
    ]

    newsletter = models.ForeignKey(NewsletterSettings, verbose_name='newsletter', on_delete=models.CASCADE)
    last_attempt = models.DateTimeField(verbose_name='last_attempt', **NULLABLE)
    attempt_status = models.CharField(max_length=12, choices=ATTEMPT_STATUS_CHOICES, verbose_name='attempt_status',
                                      **NULLABLE)
    email_server_response = models.TextField(verbose_name='email_server_response', **NULLABLE)

    def __str__(self):
        return f'{self.newsletter} (last attempt - {self.last_attempt}, {self.attempt_status})'

    class Meta:
        verbose_name = 'Newsletter Attempt'
        verbose_name_plural = 'Newsletter Attempts'


class NewsletterContent(models.Model):
    newsletter = models.ForeignKey(NewsletterSettings, on_delete=models.CASCADE)
    newsletter_subject = models.CharField(max_length=100, verbose_name='newsletter_subject')
    newsletter_content = models.TextField(verbose_name='newsletter_content')

    def __str__(self):
        return f'{self.newsletter} {self.newsletter_subject}'

    class Meta:
        verbose_name = 'Newsletter Content'
        verbose_name_plural = 'Newsletter Content'
