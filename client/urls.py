from django.urls import path

from client.apps import ClientConfig
from client.views import (ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView,
                          CityCreateView)

app_name = ClientConfig.name

urlpatterns = [
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/get/<str:slug>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client_form'),
    path('clients/city/create/', CityCreateView.as_view(), name='city_form'),
    path('clients/update/<str:slug>/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/delete/<str:slug>/', ClientDeleteView.as_view(), name='client_delete')
]
