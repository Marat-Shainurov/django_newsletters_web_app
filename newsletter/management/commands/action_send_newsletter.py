from django.core.management import BaseCommand

from newsletter.services import send_newsletter


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('newsletter_id', type=int, help='ID of the newsletter to be sent.')

    def handle(self, *args, **options):
        newsletter_id = options['newsletter_id']
        send_newsletter(newsletter_id)
