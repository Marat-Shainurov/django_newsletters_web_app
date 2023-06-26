from django.views import generic

from newsletter.models import NewsletterAttempts, Newsletter


class NewsletterAttemptsListView(generic.ListView):
    model = NewsletterAttempts
    ordering = ('-last_attempt',)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Newsletter attempts'
        context['all_newsletters'] = Newsletter.objects.all()
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()

        if 'filter_newsletter' in self.request.GET:
            newsletter_pk = self.request.GET.get('pk_filter_newsletter')
            newsletter = Newsletter.objects.get(pk=newsletter_pk)
            queryset = queryset.filter(newsletter=newsletter)

        return queryset


class NewsletterAttemptsDetailView(generic.DetailView):
    model = NewsletterAttempts

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Newsletters attempt detail'
        return context
