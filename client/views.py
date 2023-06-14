from django.urls import reverse_lazy, reverse
from django.views import generic

from client.forms import ClientForm
from client.models import Client


class ClientListView(generic.ListView):
    model = Client


class ClientDetailView(generic.DetailView):
    model = Client


class ClientCreateView(generic.CreateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('client:client_detail', kwargs={'slug': self.object.slug})


class ClientUpdateView(generic.UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('client:client_detail', kwargs={'slug': self.object.slug})


class ClientDeleteView(generic.DeleteView):
    model = Client
    success_url = reverse_lazy('client:client_list')
