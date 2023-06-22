import logging

from django.core.management import BaseCommand

from newsletter.services import send_newsletter

logger = logging.getLogger('custom_command')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('newsletter_id', type=int, help='ID of the newsletter to be sent.')

    def handle(self, *args, **options):
        newsletter_id = options['newsletter_id']
        send_newsletter(newsletter_id)
        logger.info(f'Emails have been sent to signed up clients. Newsletter id - "{newsletter_id}"')
