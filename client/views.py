from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from client.forms import ClientForm
from client.models import Client


class ClientListView(LoginRequiredMixin, generic.ListView):
    model = Client
    ordering = ('client_user', 'pk',)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Clients list'
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_manager:
            return queryset
        else:
            queryset = queryset.filter(client_user=user)
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
            self.object.client_user = self.request.user
            self.object.save()
            return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = 'Create a client'
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
