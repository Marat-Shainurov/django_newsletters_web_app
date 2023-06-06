from django.shortcuts import render
from django.views import generic

from client.models import Client


class ClientListView(generic.ListView):
    model = Client
