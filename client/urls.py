from django.urls import path
from django.views.decorators.cache import cache_page

from client.apps import ClientConfig
from client.views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView

app_name = ClientConfig.name

urlpatterns = [
    path('list/', ClientListView.as_view(), name='client_list'),
    path('list/<str:slug>/', cache_page(60)(ClientDetailView.as_view()), name='client_detail'),
    path('create/', ClientCreateView.as_view(), name='client_form'),
    path('list/update/<str:slug>/', ClientUpdateView.as_view(), name='client_update'),
    path('list/delete/<str:slug>/', ClientDeleteView.as_view(), name='client_delete')
]
