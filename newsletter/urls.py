from django.urls import path

from newsletter.apps import NewsletterConfig
from newsletter.views import NewsletterListView

app_name = NewsletterConfig.name

urlpatterns = [
    path('', NewsletterListView.as_view(), name='newsletter_list'),
]