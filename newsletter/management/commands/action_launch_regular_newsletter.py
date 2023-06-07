from django.core.management import BaseCommand, call_command
from django.shortcuts import get_object_or_404

from config import settings
from newsletter.models import Newsletter
from newsletter.services import send_newsletter


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('newsletter_id', type=int, help='ID of the newsletter to be launched.')

    def handle(self, *args, **options):
        newsletter_id = options['newsletter_id']
        newsletter_to_be_sent = get_object_or_404(Newsletter, pk=newsletter_id)
        newsletter_regularity = newsletter_to_be_sent.regularity

        cronjobs = getattr(settings, 'CRONJOBS', [])

        for cronjob in cronjobs:
            cronjob_regularity = cronjob[3]['regularity']
            if newsletter_regularity == cronjob_regularity:
                # run the needed job somehow!!!
                send_newsletter(newsletter_to_be_sent.pk)
