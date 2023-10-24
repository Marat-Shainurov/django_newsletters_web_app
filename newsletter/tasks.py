import json
import logging
from datetime import timedelta, datetime

from celery import shared_task
from django.shortcuts import get_object_or_404
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule

from newsletter.models import Newsletter
from newsletter.services import send_newsletter

logger = logging.getLogger('custom_command')


@shared_task
def send_newsletter_task(newsletter_id: str) -> None:
    """Sets True or False to the 'is_paid' field of the Payment model's objects depending on the payment status."""
    send_newsletter(newsletter_id)
    logger.info(f'Emails have been sent to signed up clients. Newsletter id - "{newsletter_id}"')


def set_regular_newsletter_schedule(newsletter_id) -> None:
    newsletter_to_send = get_object_or_404(Newsletter, pk=newsletter_id)
    newsletter_regularity = newsletter_to_send.regularity.mode_settings
    newsletter_from = newsletter_to_send.start_campaign
    newsletter_until = newsletter_to_send.finish_campaign
    campaign_duration = newsletter_until - newsletter_until
    actual_time = datetime.utcnow()

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
            name=f'Launch regular newsletter "{newsletter_id}"',
            task='newsletter.tasks.send_newsletter_task',
            args=json.dumps([newsletter_id, ]),
            kwargs={},
            expires=datetime.utcnow() + timedelta(days=campaign_duration.days)
        )
