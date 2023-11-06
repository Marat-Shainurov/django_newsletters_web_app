from datetime import datetime

import pytz
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django_celery_beat.models import PeriodicTask

from config import settings
from newsletter.models import Newsletter
from newsletter.tasks import set_regular_newsletter_schedule, disable_launched_newsletter_task, set_disabler_schedule, \
    send_newsletter_task
from users.models import User


@login_required
def regular_newsletter_manager(request):
    if request.method == 'POST':
        if 'newsletter_launch' in request.POST:
            newsletter_pk = request.POST.get('pk_newsletter_launch')
            newsletter = Newsletter.objects.get(pk=newsletter_pk)
            start_campaign = newsletter.start_campaign
            actual_time = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
            if start_campaign < actual_time:
                return redirect(
                    reverse('newsletter:invalid_newsletter_settings', kwargs={'slug': newsletter.slug}))
            else:
                set_regular_newsletter_schedule.delay(newsletter_pk)
                set_disabler_schedule(newsletter_pk)
                return redirect(reverse('newsletter:newsletter_list'))
        if 'newsletter_remove' in request.POST:
            if not request.user.has_perm('newsletter.remove_regular_newsletter'):
                raise Http404('You don\'t have access to this action! PLease contact your manager.')
            newsletter_pk = request.POST.get('pk_newsletter_remove')
            disable_launched_newsletter_task(newsletter_pk)
            return redirect(reverse('newsletter:newsletter_list'))
        if 'newsletter_one_off' in request.POST:
            newsletter_pk = request.POST.get('newsletter_one_off')
            send_newsletter_task(newsletter_pk)
            return redirect(reverse('newsletter:attempts_list'))
    else:
        user = request.user
        available_user_newsletters = Newsletter.objects.filter(newsletter_user=user, status='created')
        all_newsletters_launched = Newsletter.objects.filter(status='launched')
        all_newsletters_total = Newsletter.objects.all()
        context = {'available_user_newsletters': available_user_newsletters,
                   'newsletters_list_launched': all_newsletters_launched,
                   'page_title': 'Launch newsletter', 'all_newsletters_total': all_newsletters_total}
        return render(request, 'newsletter/control_panel.html', context)


@login_required
def regular_newsletters_report(request):
    periodic_tasks = PeriodicTask.objects.all()
    all_newsletters = Newsletter.objects.all()
    tasks_status = {}
    for task in periodic_tasks:
        task_args_newsletter_pk = task.args
        if not task.one_off and not task_args_newsletter_pk == '[]':
            newsletter = all_newsletters.filter(pk=eval(task_args_newsletter_pk)[0]).first()
            tasks_status[eval(task.args)[0]] = {
                'newsletter_id': newsletter.pk,
                'newsletter_title': newsletter.newsletter,
                'schedule': task.crontab.human_readable,
                'total_run_count': task.total_run_count,
                'start_time': task.start_time,
                'finish_time': newsletter.finish_campaign,
                'newsletter_user': newsletter.newsletter_user.email,
                'enabled': task.enabled
            }

    if 'filter_form' in request.GET:
        newsletter_pk = request.GET.get('filter_newsletter')
        user_email = request.GET.get('email_filter_user')
        if newsletter_pk == 'all' and user_email != 'all':
            tasks_status = {k: v for k, v in tasks_status.items() if v['newsletter_user'] == user_email}
        elif newsletter_pk != 'all' and user_email == 'all':
            tasks_status = {k: v for k, v in tasks_status.items() if k == newsletter_pk}
        elif user_email != 'all' and newsletter_pk != 'all':
            tasks_status = {k: v for k, v in tasks_status.items() if k == newsletter_pk}
            tasks_status = {k: v for k, v in tasks_status.items() if v['newsletter_user'] == user_email}

    all_newsletters = Newsletter.objects.all()
    all_users = User.objects.all()
    context = {'tasks_status': tasks_status, 'all_newsletters': all_newsletters, 'all_users': all_users}

    return render(request, 'newsletter/regular_newsletters_report.html', context)


def invalid_newsletter_settings(request, slug):
    newsletter = Newsletter.objects.get(slug=slug)
    context = {
        'actual_time': datetime.now(tz=pytz.timezone(settings.TIME_ZONE)),
        'newsletter': newsletter,
        'message': f'Please, check and edit the "{newsletter.newsletter}" newsletter settings. '
                   f'"start_campaign" cannot be earlier that actual time'
    }
    return render(request, 'newsletter/invalid_regular_newsletter.html', context)
