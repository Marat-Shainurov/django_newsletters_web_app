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
            if 'filter_form' in self.request.GET:
                newsletter_pk = self.request.GET.get('filter_newsletter')
                if newsletter_pk != 'all':
                    newsletter = Newsletter.objects.get(pk=newsletter_pk)
                    queryset = queryset.filter(newsletter=newsletter)
                else:
                    return queryset
            return queryset

        else:
            if 'filter_form' in self.request.GET:
                newsletter_pk = self.request.GET.get('filter_newsletter')
                user_email = self.request.GET.get('email_filter_user')
                if newsletter_pk == 'all' and user_email != 'all':
                    user_to_filter = User.objects.get(email=user_email)
                    user_newsletters = Newsletter.objects.filter(newsletter_user=user_to_filter)
                    queryset = queryset.filter(newsletter__in=user_newsletters)
                elif user_email == 'all' and newsletter_pk != 'all':
                    newsletter = Newsletter.objects.get(pk=newsletter_pk)
                    queryset = queryset.filter(newsletter=newsletter)
                elif newsletter_pk != 'all' and user_email != 'all' :
                    user_to_filter = User.objects.get(email=user_email)
                    user_newsletters = Newsletter.objects.filter(newsletter_user=user_to_filter)
                    queryset = queryset.filter(newsletter__in=user_newsletters)
                    newsletter = Newsletter.objects.get(pk=newsletter_pk)
                    queryset = queryset.filter(newsletter=newsletter)
                else:
                    return queryset
            return queryset


class NewsletterAttemptsDetailView(LoginRequiredMixin, generic.DetailView):
    model = NewsletterAttempts

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Newsletters attempt detail'
        return context
