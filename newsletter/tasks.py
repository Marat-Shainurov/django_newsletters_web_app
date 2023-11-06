import json
import logging
from datetime import datetime

import pytz
from celery import shared_task, current_task
from django.shortcuts import get_object_or_404
from django_celery_beat.models import PeriodicTask, CrontabSchedule, ClockedSchedule

from config import settings
from newsletter.models import Newsletter
from newsletter.services import send_newsletter

logger = logging.getLogger('custom_command')


@shared_task
def send_newsletter_task(newsletter_pk: str) -> None:
    """Sends emails to the signed up clients of the request user."""
    send_newsletter(newsletter_pk)
    logger.info(f'Emails have been sent to the signed up clients. Newsletter id - "{newsletter_pk}"')


@shared_task
def disable_launched_newsletter_task(newsletter_pk: str) -> None:
    """Sets the 'task.enable' field to False"""
    task = PeriodicTask.objects.get(name=f'Regular newsletter {newsletter_pk}')
    newsletter = get_object_or_404(Newsletter, pk=newsletter_pk)
    task.enabled = False
    current_task.ignore_validation = True
    newsletter.status = 'finished'
    newsletter.save()
    current_task.ignore_validation = False
    task.save()
    logger.info(f'Regular newsletter {newsletter_pk} has been disabled.')

    task_disabler = PeriodicTask.objects.get(name=f'Disable newsletter {newsletter_pk}')
    task_disabler.enabled = False
    task_disabler.save()


@shared_task()
def set_regular_newsletter_schedule(newsletter_pk) -> None:
    """Sets a schedule for a new  regular newsletter."""
    newsletter_to_send = get_object_or_404(Newsletter, pk=newsletter_pk)
    newsletter_regularity = newsletter_to_send.regularity.mode_settings
    newsletter_from = newsletter_to_send.start_campaign
    newsletter_until = newsletter_to_send.finish_campaign
    actual_time = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))

    if actual_time > newsletter_from or actual_time > newsletter_until:
        logger.info(
            f"\nActual time is later than the 'finish_campaign' or 'start_campaign' fields' value)")
    else:
        regularity_list = newsletter_regularity.split()
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=regularity_list[0], hour=regularity_list[1], day_of_month=regularity_list[2],
            month_of_year=regularity_list[3], day_of_week=regularity_list[4],
        )
        PeriodicTask.objects.create(
            crontab=schedule,
            start_time=newsletter_from,
            name=f'Regular newsletter {newsletter_pk}',
            task='newsletter.tasks.send_newsletter_task',
            args=json.dumps([newsletter_pk, ]),
            kwargs={},
        )
        newsletter_to_send.status = 'launched'
        newsletter_to_send.save()


@shared_task()
def set_disabler_schedule(newsletter_pk):
    newsletter_to_enable = get_object_or_404(Newsletter, pk=newsletter_pk)
    newsletter_until = newsletter_to_enable.finish_campaign
    schedule, created = ClockedSchedule.objects.get_or_create(
        clocked_time=newsletter_until
    )
    PeriodicTask.objects.create(
        clocked=schedule,
        one_off=True,
        name=f'Disable newsletter {newsletter_pk}',
        task='newsletter.tasks.disable_launched_newsletter_task',
        args=json.dumps([newsletter_pk, ]),
        kwargs={},
    )
