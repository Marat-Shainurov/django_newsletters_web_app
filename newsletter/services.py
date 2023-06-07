from django.conf import settings
from django.core.mail import send_mail

from client.models import Client
from newsletter.models import Newsletter


def send_newsletter(newsletter_id):
    clients_to_be_informed = Client.objects.filter(is_signed_up=True)
    newsletter_to_be_sent = Newsletter.objects.get(pk=newsletter_id)
    send_mail(
        f'{newsletter_to_be_sent.subject}',
        f'{newsletter_to_be_sent.content}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[x.email for x in clients_to_be_informed]
    )
