import sys
from datetime import datetime
from pathlib import Path

from crontab import CronTab
from dateutil import parser
from dateutil.tz import tz
from django.core.management import BaseCommand, call_command
from django.shortcuts import get_object_or_404

from config import settings
from config.settings import BASE_DIR
from newsletter.models import Newsletter


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('newsletter_id', type=int, help='ID of the newsletter to be launched.')

    def handle(self, *args, **options):
        newsletter_id = options['newsletter_id']
        newsletter_to_be_sent: Newsletter = get_object_or_404(Newsletter, pk=newsletter_id)
        newsletter_regularity = newsletter_to_be_sent.regularity
        newsletter_from = parser.parse(newsletter_to_be_sent.start_campaign.strftime("%Y-%m-%d %H:%M:%S")).replace(tzinfo=None)
        newsletter_until = parser.parse(newsletter_to_be_sent.finish_campaign.strftime("%Y-%m-%d %H:%M:%S")).replace(tzinfo=None)
        timezone = tz.gettz(settings.TIME_ZONE)
        actual_time = datetime.now(timezone).replace(tzinfo=None)

        regularity_modes = {'daily': '55 13 * * *', 'weekly': '0 12 * * 1', 'monthly': '0 12 1 * *'}

        python_executable = Path(sys.executable)
        manage_py = BASE_DIR / 'manage.py'

        for mode in regularity_modes:
            if mode == newsletter_regularity:

                if actual_time > newsletter_from:
                    # calls immediate sending via "action_send_newsletter"
                    call_command('action_send_newsletter', f'{newsletter_id}')
                    print(f'Actual time ({actual_time}) is later than the "start_campaign" value ({newsletter_from}). '
                          f'The newsletter has been sent right away.')

                    # sets a new cron job from the closest date, following the cron job schedule
                    cron = CronTab(user=True)
                    command = f'{python_executable} {manage_py} action_send_newsletter {newsletter_id}'
                    job = cron.new(command=command)
                    job.setall(regularity_modes[mode])
                    cron.write()
                    print(f'\nCron job is added successfully. \nNewsletter regularity mode - {newsletter_regularity}')
                    print(f'Campaign duration - from "{newsletter_from}", until "{newsletter_until}"')

                    newsletter_to_be_sent.status = 'launched'
                    newsletter_to_be_sent.save()
