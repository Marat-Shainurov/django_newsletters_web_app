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
            'daily': '50 19 * * *',
            'weekly': '0 12 * * 1',
            'monthly': '0 12 1 * *'
        }

        for mode in regularity_modes:
            if mode == newsletter_regularity:
                cron = CronTab(user=True)
                # command = f'\\wsl$\\Ubuntu\\home\\marat_shainurov\\django_cw\\venv\\bin\\python \\wsl$\\Ubuntu\\home\\marat_shainurov\\django_cw\\manage.py action_send_newsletter {newsletter_id}'
                # command = f'/mnt/wsl/Ubuntu/home/marat_shainurov/django_cw/venv/bin/python /mnt/wsl/Ubuntu/home/marat_shainurov/django_cw/manage.py action_send_newsletter {newsletter_id}'
                command = f'python manage.py action_send_newsletter {newsletter_id}'
                job = cron.new(command=command)
                job.setall(regularity_modes[mode])
                cron.write()
                print('Cron job is added successfully')
