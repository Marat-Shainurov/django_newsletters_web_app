from django.urls import path

from newsletter.apps import NewsletterConfig
from newsletter.views import NewsletterListView, NewsletterDetailView, NewsletterCreateView, NewsletterUpdateView, \
    NewsletterDeleteView, NewsletterAttemptsListView, NewsletterAttemptsDetailView

app_name = NewsletterConfig.name

urlpatterns = [
    path('', NewsletterListView.as_view(), name='newsletter_list'),
    path('create/', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('<str:slug>/', NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('update/<str:slug>/', NewsletterUpdateView.as_view(), name='newsletter_update'),
    path('delete/<str:slug>', NewsletterDeleteView.as_view(), name='newsletter_delete'),
    path('newsletters/attempts-report/', NewsletterAttemptsListView.as_view(), name='attempts_list'),
    path('newsletters/report/<int:pk>/', NewsletterAttemptsDetailView.as_view(), name='attempt_responses_detail')
]
