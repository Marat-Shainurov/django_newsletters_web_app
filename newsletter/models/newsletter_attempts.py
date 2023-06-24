from django.db import models

from newsletter.models.newsletter import Newsletter

NULLABLE = {'blank': True, 'null': True}


class NewsletterAttempts(models.Model):
    ATTEMPT_STATUS_CHOICES = [
        ('success', 'Success'),
        ('failure', 'Failure'),
        ('in_progress', 'In_progress'),
    ]

    newsletter = models.ForeignKey(Newsletter, verbose_name='newsletter', on_delete=models.CASCADE,
                                   related_name='newsletter_attempt')
    last_attempt = models.DateTimeField(verbose_name='last_attempt', **NULLABLE)
    attempt_status = models.CharField(max_length=12, choices=ATTEMPT_STATUS_CHOICES, verbose_name='attempt_status',
                                      **NULLABLE, default='in_progress')
    comment = models.TextField(verbose_name='Error message or comment', **NULLABLE)

    def __str__(self):
        return f'{self.newsletter}'

    class Meta:
        verbose_name = 'Newsletter Attempt'
        verbose_name_plural = 'Newsletter Attempts'
