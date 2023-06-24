import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from blog.models import Blog
from client.models import Client
from newsletter.models import Newsletter, NewsletterAttempts


@login_required(login_url='users:login')
def index(request):
    all_newsletters = Newsletter.objects.filter(is_active=True)
    all_newsletters_launched = Newsletter.objects.filter(status='launched')
    all_newsletters_created = Newsletter.objects.filter(status='created')
    all_newsletters_finished = Newsletter.objects.filter(status='finished')
    all_attempts = NewsletterAttempts.objects.all()
    attempts_success = NewsletterAttempts.objects.filter(attempt_status='success')
    success_ratio = str(round(((attempts_success.count() / all_attempts.count()) * 100), 0)) + '%'
    all_clients = Client.objects.all()
    all_clients_signed_up = Client.objects.filter(is_signed_up=True)
    signing_up_ratio = str(round(((all_clients_signed_up.count() / all_clients.count()) * 100), 0)) + '%'
    all_blogs = Blog.objects.all()
    blogs_to_show = [all_blogs[x] for x in range(all_blogs.count())]
    random.shuffle(blogs_to_show)

    context = {
        'all_newsletters': all_newsletters,
        'all_newsletters_launched': all_newsletters_launched,
        'all_newsletters_created': all_newsletters_created,
        'all_newsletters_finished': all_newsletters_finished,
        'all_attempts': all_attempts,
        'attempts_success': attempts_success,
        'success_ratio': success_ratio,
        'all_clients': all_clients,
        'all_clients_signed_up': all_clients_signed_up,
        'signing_up_ratio': signing_up_ratio,
        'blogs_to_show': blogs_to_show[:3],
        'page_title': 'Main page'
    }
    return render(request, 'newsletter/index.html', context)
