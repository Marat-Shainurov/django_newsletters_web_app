from django.urls import path

from newsletter.apps import NewsletterConfig
from newsletter.views import NewsletterListView, NewsletterDetailView, NewsletterCreateView

app_name = NewsletterConfig.name

urlpatterns = [
    path('', NewsletterListView.as_view(), name='newsletter_list'),
    path('create/', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('<str:slug>/', NewsletterDetailView.as_view(), name='newsletter_detail'),
]
