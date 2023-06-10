import sys
from pathlib import Path

from crontab import CronTab
from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from config.settings import BASE_DIR
from newsletter.models import Newsletter


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('newsletter_id', type=int, help='ID of the newsletter to be launched.')

    def handle(self, *args, **options):
        newsletter_id = options['newsletter_id']
        newsletter_to_be_sent = get_object_or_404(Newsletter, pk=newsletter_id)
        newsletter_regularity = newsletter_to_be_sent.regularity

        regularity_modes = {
            'daily': '10 12 * * *',
            'weekly': '0 12 * * 1',
            'monthly': '0 12 1 * *'
        }

        python_executable = Path(sys.executable)
        manage_py = BASE_DIR / 'manage.py'

        for mode in regularity_modes:
            if mode == newsletter_regularity:
                cron = CronTab(user=True)
                command = f'{python_executable} {manage_py} action_send_newsletter {newsletter_id}'
                job = cron.new(command=command)
                job.setall(regularity_modes[mode])
                cron.write()
                print('Cron job is added successfully')
                print(f'newsletter regularity mode - {newsletter_regularity}')
