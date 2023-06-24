import re
from datetime import datetime
from smtplib import SMTPException

from crontab import CronTab
from dateutil.tz import tz
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.core.management import call_command
from django.core.validators import EmailValidator, ValidationError

from client.models import Client
from newsletter.models import Newsletter, NewsletterAttempts, EmailServerResponse


def send_newsletter(newsletter_id):
    clients_to_be_informed = Client.objects.filter(is_signed_up=True)
    newsletter_to_send = Newsletter.objects.get(pk=newsletter_id)
    recipient_list = [x.email for x in clients_to_be_informed]
    timezone = tz.gettz(settings.TIME_ZONE)
    actual_time = datetime.now(timezone)

    new_attempt = NewsletterAttempts.objects.create(newsletter=newsletter_to_send, last_attempt=actual_time)
    email_validator = EmailValidator()

    if len(recipient_list) == 0:
        new_attempt.attempt_status = 'failure'
        new_attempt.comment = 'No emails to inform'
        new_attempt.save()

    informed_clients_count = 0

    for address in recipient_list:
        new_response_obj = EmailServerResponse.objects.create(attempt=new_attempt, recipient_email=address)

        try:
            email_validator(address)
            send_mail(
                f'{newsletter_to_send.subject}',
                f'{newsletter_to_send.content}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[address],
            )
        except (SMTPException, BadHeaderError, ValidationError) as error:
            new_response_obj.response = str(error)
        except Exception as e:
            new_response_obj.response = str(e)
        else:
            new_response_obj.response = 'Successful sending.'
            informed_clients_count += 1
        finally:
            new_response_obj.save()

    new_attempt.attempt_status = 'success'
    new_attempt.comment = f'{informed_clients_count} clients have been informed out of {len(recipient_list)}'
    new_attempt.save()

from pathlib import Path
import sys

def get_launched_cron_jobs():
    cron = CronTab(user=True)

    res_cron_jobs = {}
    cron_jobs = []

    for job in cron.lines:
        if job != '':
            cron_jobs.append(str(job.slices) + ' ' + str(job.command))

    for j in cron_jobs:
        job_id = j[-1]
        newsletter = Newsletter.objects.get(pk=job_id)
        match_action_type = re.search('remove', j.lower())
        if match_action_type:
            res_cron_jobs[' '.join(j.split()[:5])] = ['removal', job_id, newsletter]
        else:
            res_cron_jobs[' '.join(j.split()[:5])] = ['regular', job_id, newsletter]

    return res_cron_jobs
