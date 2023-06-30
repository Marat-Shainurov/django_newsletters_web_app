from django.contrib.auth.decorators import login_required, permission_required
from django.core.management import call_command
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from newsletter.models import Newsletter
from newsletter.services import get_launched_cron_jobs

@login_required
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

@login_required
def regular_newsletter_manager(request):
    if request.method == 'POST':
        if 'newsletter_launch' in request.POST:
            newsletter = request.POST.get('pk_newsletter_launch')
            call_command('action_launch_regular_newsletter', f'{newsletter}')
            return redirect(reverse('users:regular_newsletter_manager'))
        if 'newsletter_remove' in request.POST:
            if not request.user.has_perm('newsletter.remove_regular_newsletter'):
                raise Http404('You don\'t have access to this action! PLease contact your manager.')
            newsletter = request.POST.get('pk_newsletter_remove')
            call_command('action_remove_cronjob', f'{newsletter}')
            return redirect(reverse('users:regular_newsletter_manager'))
    else:
        user = request.user
        all_newsletters_new = Newsletter.objects.exclude(status='launched').filter(newsletter_user=user)
        all_newsletters_rem = Newsletter.objects.filter(status='launched')
        cron_jobs = get_launched_cron_jobs()
        all_newsletters_total = Newsletter.objects.all()
        context = {'all_newsletters_new': all_newsletters_new, 'newsletters_list_rem': all_newsletters_rem,
                   'cron_jobs': cron_jobs, 'page_title': 'Launch newsletter',
                   'all_newsletters_total': all_newsletters_total}
        return render(request, 'users/regular_newsletter_manager.html', context)
