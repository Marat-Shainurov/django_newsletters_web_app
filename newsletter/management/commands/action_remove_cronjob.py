import logging
import sys
from pathlib import Path

from crontab import CronTab
from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from config.settings import BASE_DIR
from newsletter.models import Newsletter


class Command(BaseCommand):
    python_executable = Path(sys.executable)
    manage_py = BASE_DIR / 'manage.py'

    def add_arguments(self, parser):
        parser.add_argument('cronjob_id', type=int, help='Cronjob\'s id to remove.')

    def handle(self, *args, **options):
        cronjob_id = options['cronjob_id']
        cron = CronTab(user=True)
        cronjob_to_remove = cron.find_comment(f'{cronjob_id}')
        cron.remove(cronjob_to_remove)
        cron.write()

        newsletter = get_object_or_404(Newsletter, pk=cronjob_id)
        newsletter.status = 'finished'
        newsletter.save()
        logging.info(f'The "{cronjob_id}" cronjob has been removed successfully')
