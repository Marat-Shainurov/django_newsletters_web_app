from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.urls import reverse_lazy, reverse
from django.views import generic

from client.models import City
from newsletter.forms import NewsletterForm
from newsletter.models import Newsletter
from users.models import User


class NewsletterListView(LoginRequiredMixin, generic.ListView):
    model = Newsletter
    ordering = ('newsletter_user', 'pk')

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_active=True)

        user = self.request.user
        group = Group.objects.get(name='manager')
        if group not in user.groups.all():
            queryset = queryset.filter(user=user)

        if 'filter_form' in self.request.GET:
            status = self.request.GET.get('filter_status')
            user_email = self.request.GET.get('email_filter_user')
            if status == 'all' and user_email != 'all':
                user_to_filter = User.objects.get(email=user_email)
                queryset = queryset.filter(newsletter_user=user_to_filter)
            elif user_email == 'all' and status != 'all':
                queryset = queryset.filter(status=status)
            elif user_email != 'all' and status != 'all':
                user_to_filter = User.objects.get(email=user_email)
                queryset = queryset.filter(status=status, newsletter_user=user_to_filter)
            else:
                return queryset

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Newsletters list'
        context['all_cities'] = City.objects.all()
        context['all_users'] = User.objects.all()
        context['all_statuses'] = [status[0] for status in Newsletter.STATUS_CHOICE]
        return context


class NewsletterDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newsletter

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Newsletters detail'
        return context


class NewsletterCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newsletter
    form_class = NewsletterForm
    extra_context = {'page_title': 'Create a newsletter'}

    def get_success_url(self):
        return reverse('newsletter:newsletter_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        self.object = form.save()
        if form.is_valid():
            self.object.newsletter_user = self.request.user
            self.object.save()
            return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newsletter
    form_class = NewsletterForm

    def get_success_url(self):
        return reverse('newsletter:newsletter_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Update newsletter'
        return context


class NewsletterDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newsletter
    success_url = reverse_lazy('newsletter:newsletter_list')
    extra_context = {'page_title': 'Delete newsletter'}
