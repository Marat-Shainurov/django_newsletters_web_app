from django.urls import path

from client.apps import ClientConfig
from client.views import ClientListView, ClientDetailView

app_name = ClientConfig.name

urlpatterns = [
    path('all/', ClientListView.as_view(), name='client_list'),
    path('all/<str:slug>/', ClientDetailView.as_view(), name='client_detail'),
]
