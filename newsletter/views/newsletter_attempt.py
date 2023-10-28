from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.views import generic

from newsletter.models import NewsletterAttempts, Newsletter
from users.models import User


class NewsletterAttemptsListView(LoginRequiredMixin, generic.ListView):
    model = NewsletterAttempts
    ordering = ('-last_attempt',)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Newsletter attempts'
        context['all_newsletters'] = Newsletter.objects.all()
        context['all_users'] = User.objects.all()
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        user = self.request.user
        group = Group.objects.get(name='manager')
        if group not in user.groups.all():
            user_newsletters = Newsletter.objects.filter(newsletter_user=user)
            queryset = queryset.filter(newsletter__in=user_newsletters)

        if 'filter_newsletter' in self.request.GET:
            newsletter_pk = self.request.GET.get('pk_filter_newsletter')
            if newsletter_pk == 'all' or newsletter_pk == 'Select newsletter:':
                return queryset
            newsletter = Newsletter.objects.get(pk=newsletter_pk)
            queryset = queryset.filter(newsletter=newsletter)
        if 'filter_users' in self.request.GET:
            user_email = self.request.GET.get('email_filter_user')
            if user_email == 'all' or user_email == 'Select user:':
                return queryset
            newsletters = Newsletter.objects.filter(newsletter_user=User.objects.get(email=user_email))
            queryset = queryset.filter(newsletter__in=newsletters)

        return queryset


class NewsletterAttemptsDetailView(LoginRequiredMixin, generic.DetailView):
    model = NewsletterAttempts

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Newsletters attempt detail'
        return context
