from django.db import models

from newsletter.models.newsletter_attempts import NewsletterAttempts

NULLABLE = {'blank': True, 'null': True}


class EmailServerResponse(models.Model):
    attempt = models.ForeignKey(NewsletterAttempts, verbose_name='newsletter_attempt', on_delete=models.CASCADE,
                                related_name='email_response')
    recipient_email = models.EmailField(verbose_name='recipient_email')
    response = models.TextField(verbose_name='email_server_response', **NULLABLE)

    def __str__(self):
        return f'{self.attempt} ({self.recipient_email}, response - {self.response})'

    class Meta:
        verbose_name = 'Response'
        verbose_name_plural = 'Responses'
