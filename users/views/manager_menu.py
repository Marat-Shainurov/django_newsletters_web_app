from django.core.management import call_command
from django.shortcuts import render, redirect
from django.urls import reverse

from newsletter.models import Newsletter
from newsletter.services import get_launched_cron_jobs


def send_newsletter_manager(request):
    if request.method == 'POST':
        newsletter = request.POST.get('newsletter')
        call_command('action_send_newsletter', f'{newsletter}')
        return redirect(reverse('newsletter:newsletter_list'))
    else:
        user = request.user
        all_newsletters = Newsletter.objects.filter(newsletter_user=user)
        context = {'newsletters_list': all_newsletters, 'user': user, 'page_title': 'Send newsletter'}
        return render(request, 'users/send_newsletter_manager.html', context)


def regular_newsletter_manager(request):
    if request.method == 'POST':
        if 'newsletter_launch' in request.POST:
            newsletter = request.POST.get('pk_newsletter_launch')
            call_command('action_launch_regular_newsletter', f'{newsletter}')
            return redirect(reverse('users:regular_newsletter_manager'))
        if 'newsletter_remove' in request.POST:
            newsletter = request.POST.get('pk_newsletter_remove')
            call_command('action_remove_cronjob', f'{newsletter}')
            return redirect(reverse('users:regular_newsletter_manager'))
    else:
        user = request.user
        all_newsletters = Newsletter.objects.filter(newsletter_user=user)
        cron_jobs = get_launched_cron_jobs()
        all_newsletters_total = Newsletter.objects.all()
        context = {'newsletters_list': all_newsletters, 'cron_jobs': cron_jobs, 'page_title': 'Launch newsletter',
                   'all_newsletters_total': all_newsletters_total}
        return render(request, 'users/regular_newsletter_manager.html', context)
