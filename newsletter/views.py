from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from client.models import Client
from newsletter.forms import NewsletterForm
from newsletter.models import Newsletter, NewsletterAttempts


class NewsletterListView(generic.ListView):
    model = Newsletter

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_active=True)
        return queryset


class NewsletterDetailView(generic.DetailView):
    model = Newsletter


class NewsletterCreateView(generic.CreateView):
    model = Newsletter
    form_class = NewsletterForm

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


class NewsletterDeleteView(generic.DeleteView):
    model = Newsletter
    success_url = reverse_lazy('newsletter:newsletter_list')


class NewsletterAttemptsListView(generic.ListView):
    model = NewsletterAttempts


class NewsletterAttemptsDetailView(generic.DetailView):
    model = NewsletterAttempts


def index(request):
    all_newsletters = Newsletter.objects.exclude(status='finished')
    all_newsletters_launched = Newsletter.objects.filter(status='launched')
    all_attempts = NewsletterAttempts.objects.all()
    all_clients = Client.objects.all()
    all_clients_signed_up = Client.objects.filter(is_signed_up=True)
    context = {
        'all_newsletters': all_newsletters,
        'all_newsletters_launched': all_newsletters_launched,
        'all_attempts': all_attempts,
        'all_clients': all_clients,
        'all_clients_signed_up': all_clients_signed_up,
    }
    return render(request, 'newsletter/index.html', context)
