from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from newsletter.models import Newsletter

from crontab import CronTab


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('newsletter_id', type=int, help='ID of the newsletter to be launched.')

    def handle(self, *args, **options):
        newsletter_id = options['newsletter_id']
        newsletter_to_be_sent = get_object_or_404(Newsletter, pk=newsletter_id)
        newsletter_regularity = newsletter_to_be_sent.regularity

        regularity_modes = {
            'daily': '35 14 * * *',
            'weekly': '0 12 * * 1',
            'monthly': '0 12 1 * *'
        }

        for mode in regularity_modes:
            if mode == newsletter_regularity:
                cron = CronTab(user=True)
                job = cron.new(
                    command=f'C:\\Users\\m_sha\\AppData\\Local\\Microsoft\\WindowsApps\\python3.11.exe /path/to/django/project/manage.py action_send_newsletter {newsletter_id}')
                job.setall(regularity_modes[mode])
                cron.write()
                print('Cron job is added successfully')
