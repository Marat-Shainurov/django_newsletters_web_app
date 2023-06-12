from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from newsletter.forms import NewsletterForm
from newsletter.models import Newsletter


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


class NewsletterUpdateView(generic.UpdateView):
    model = Newsletter
    fields = (
        'newsletter', 'status', 'start_campaign', 'finish_campaign', 'regularity', 'subject', 'content', 'is_active')

    def get_success_url(self):
        return reverse('newsletter:newsletter_detail', kwargs={'slug': self.object.slug})


class NewsletterDeleteView(generic.DeleteView):
    model = Newsletter
    success_url = reverse_lazy('newsletter:newsletter_list')
