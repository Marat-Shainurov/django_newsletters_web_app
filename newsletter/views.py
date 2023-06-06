from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from newsletter.models import Newsletter


class NewsletterListView(generic.ListView):
    model = Newsletter


class NewsletterDetailView(generic.DetailView):
    model = Newsletter


class NewsletterCreateView(generic.CreateView):
    model = Newsletter
    fields = ('newsletter', 'start_campaign', 'finish_campaign', 'regularity', 'subject', 'content')

    def get_success_url(self):
        return reverse_lazy('newsletter:newsletter_detail', kwargs={'slug': self.object.slug})


class NewsletterUpdateView(generic.UpdateView):
    model = Newsletter
    fields = ('newsletter', 'start_campaign', 'finish_campaign', 'regularity', 'subject', 'content')

    def get_success_url(self):
        return reverse_lazy('newsletter:newsletter_detail', kwargs={'slug': self.object.slug})
