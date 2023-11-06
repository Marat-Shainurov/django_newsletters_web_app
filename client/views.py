from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from client.forms import ClientForm, CityForm
from client.models import Client, City
from users.models import User


class ClientListView(LoginRequiredMixin, generic.ListView):
    model = Client
    ordering = ('user', 'pk',)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Clients list'
        context['all_users'] = User.objects.all()
        context['all_cities'] = City.objects.all()
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_active=True)
        user = self.request.user

        group = Group.objects.get(name='manager')
        if group not in user.groups.all():
            queryset = queryset.filter(user=user)
            if 'filter_form' in self.request.GET:
                city = self.request.GET.get('filter_city')
                if city != 'all':
                    city_to_filter = City.objects.get(city=city)
                    queryset = queryset.filter(city=city_to_filter)
                else:
                    return queryset
            return queryset
        else:
            if 'filter_form' in self.request.GET:
                city = self.request.GET.get('filter_city')
                user_email = self.request.GET.get('email_filter_user')
                if city == 'all' and user_email != 'all':
                    user_to_filter = User.objects.get(email=user_email)
                    queryset = queryset.filter(user=user_to_filter)
                elif user_email == 'all' and city != 'all':
                    city_to_filter = City.objects.get(city=city)
                    queryset = queryset.filter(city=city_to_filter)
                elif user_email != 'all' and city != 'all':
                    city_to_filter = City.objects.get(city=city)
                    user_to_filter = User.objects.get(email=user_email)
                    queryset = queryset.filter(city=city_to_filter, user=user_to_filter)
                else:
                    return queryset
            return queryset

    def post(self, *args, **kwargs):

        if 'sign_up_toggle' in self.request.POST:
            pk = self.request.POST.get('pk_sign_up_toggle')
            client = Client.objects.get(pk=pk)
            client.is_signed_up = not client.is_signed_up
            client.save()

        return redirect(reverse('client:client_list'))


class ClientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Client

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Client details'
        return context


class ClientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('client:client_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        self.object = form.save()
        if form.is_valid():
            self.object.user = self.request.user
            self.object.save()
            return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Create a client'
        return context


class CityCreateView(LoginRequiredMixin, generic.CreateView):
    model = City
    form_class = CityForm

    def get_success_url(self):
        return reverse('client:client_list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Create a city'
        return context


class ClientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('client:client_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Update a client'
        return context


class ClientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Client
    success_url = reverse_lazy('client:client_list')
    extra_context = {'page_title': 'Delete a client'}
