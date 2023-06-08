from crontab import CronTab
from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from newsletter.models import Newsletter
from newsletter.services import send_newsletter


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('newsletter_id', type=int, help='ID of the newsletter to be launched.')

    def handle(self, *args, **options):
        newsletter_id = options['newsletter_id']
        newsletter_to_be_sent = get_object_or_404(Newsletter, pk=newsletter_id)
        newsletter_regularity = newsletter_to_be_sent.regularity

        if newsletter_regularity == 'daily':
            cron = CronTab(user=True)
            job = cron.new(command=f'python manage.py action_send_newsletter {newsletter_id}')
            job.minute.on(0)
            job.hour.on(9)
            cron.write()
            print('Cron job was added successfully')
