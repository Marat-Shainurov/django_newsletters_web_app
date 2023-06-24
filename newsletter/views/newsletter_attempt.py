from django.views import generic

from newsletter.models import NewsletterAttempts


class NewsletterAttemptsListView(generic.ListView):
    model = NewsletterAttempts
    ordering = ('-last_attempt',)

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
