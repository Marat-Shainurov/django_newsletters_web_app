import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from blog.models import Blog
from client.models import Client
from newsletter.forms import NewsletterForm
from newsletter.models import Newsletter, NewsletterAttempts


class NewsletterListView(generic.ListView):
    model = Newsletter
    ordering = ('newsletter_user', 'pk')

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_active=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Newsletters list'
        return context


class NewsletterDetailView(generic.DetailView):
    model = Newsletter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Newsletters detail'
        return context


class NewsletterCreateView(generic.CreateView):
    model = Newsletter
    form_class = NewsletterForm
    extra_context = {'page_title': 'Create a newsletter'}

    def get_success_url(self):
        return reverse_lazy('newsletter:newsletter_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        self.object = form.save()
        if form.is_valid():
            self.object.newsletter_user = self.request.user
            self.object.save()
            return super().form_valid(form)


class NewsletterUpdateView(generic.UpdateView):
    model = Newsletter
    form_class = NewsletterForm

    def get_success_url(self):
        return reverse('newsletter:newsletter_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Update newsletter'
        return context


class NewsletterDeleteView(generic.DeleteView):
    model = Newsletter
    success_url = reverse_lazy('newsletter:newsletter_list')
    extra_context = {'page_title': 'Delete newsletter'}


class NewsletterAttemptsListView(generic.ListView):
    model = NewsletterAttempts

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Newsletter attempts'
        return context


class NewsletterAttemptsDetailView(generic.DetailView):
    model = NewsletterAttempts

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Newsletters attempt detail'
        return context

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
