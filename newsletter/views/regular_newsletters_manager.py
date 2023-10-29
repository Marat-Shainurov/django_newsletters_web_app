from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django_celery_beat.models import PeriodicTask

from newsletter.models import Newsletter
from newsletter.tasks import set_regular_newsletter_schedule, disable_launched_newsletter_task, set_disabler_schedule, \
    send_newsletter_task
from users.models import User



@login_required
def regular_newsletter_manager(request):
    if request.method == 'POST':
        if 'newsletter_launch' in request.POST:
            newsletter_pk = request.POST.get('pk_newsletter_launch')
            set_regular_newsletter_schedule.delay(newsletter_pk)
            set_disabler_schedule(newsletter_pk)
            return redirect(reverse('newsletter:regular_newsletter_manager'))
        if 'newsletter_remove' in request.POST:
            if not request.user.has_perm('newsletter.remove_regular_newsletter'):
                raise Http404('You don\'t have access to this action! PLease contact your manager.')
            newsletter_pk = request.POST.get('pk_newsletter_remove')
            disable_launched_newsletter_task(newsletter_pk)
            return redirect(reverse('newsletter:regular_newsletter_manager'))
        if 'newsletter_one_off' in request.POST:
            newsletter_pk = request.POST.get('newsletter_one_off')
            send_newsletter_task(newsletter_pk)
            return redirect(reverse('newsletter:regular_newsletter_manager'))
    else:
        user = request.user
        available_user_newsletters = Newsletter.objects.exclude(status='launched').filter(newsletter_user=user)
        all_newsletters_launched = Newsletter.objects.filter(status='launched')
        all_newsletters_total = Newsletter.objects.all()
        context = {'available_user_newsletters': available_user_newsletters,
                   'newsletters_list_launched': all_newsletters_launched,
                   'page_title': 'Launch newsletter', 'all_newsletters_total': all_newsletters_total}
        return render(request, 'newsletter/regular_newsletter_manager.html', context)


@login_required
def regular_newsletters_report(request):
    periodic_tasks = PeriodicTask.objects.all()
    tasks_status = {}
    for task in periodic_tasks:
        newsletter = task.args
        if not task.one_off and task.enabled and not newsletter == '[]':
            newsletter = Newsletter.objects.get(pk=eval(task.args)[0])
            tasks_status[eval(task.args)[0]] = {
                'newsletter_id': newsletter.pk,
                'newsletter_title': newsletter.title,
                'schedule': task.crontab.human_readable,
                'total_run_count': task.total_run_count,
                'start_time': task.start_time,
                'finish_time': newsletter.finish_campaign,
                'newsletter_user': newsletter.newsletter_user.email
            }

    if 'filter_newsletter' in request.GET:
        newsletter_pk = request.GET.get('pk_filter_newsletter')
        if newsletter_pk == 'all' or newsletter_pk == 'Select newsletter:':
            pass
        else:
            tasks_status = {k: v for k, v in tasks_status.items() if k == newsletter_pk}
    if 'filter_users' in request.GET:
        user_email = request.GET.get('email_filter_user')
        if user_email == 'all' or user_email == 'Select user:':
            pass
        else:
            tasks_status = {k: v for k, v in tasks_status.items() if v['newsletter_user'] == user_email}

    all_newsletters = Newsletter.objects.all()
    all_users = User.objects.all()
    context = {'tasks_status': tasks_status, 'all_newsletters': all_newsletters, 'all_users': all_users}

    return render(request, 'newsletter/regular_newsletters_report.html', context)
