from django.urls import path
from django.views.decorators.cache import cache_page

from newsletter.apps import NewsletterConfig
from newsletter.views import NewsletterListView, NewsletterDetailView, NewsletterCreateView, NewsletterUpdateView, \
    NewsletterDeleteView, NewsletterAttemptsListView, NewsletterAttemptsDetailView, index

app_name = NewsletterConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('newsletters/list/', NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletters/create/', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newsletters/details/<str:slug>/', cache_page(60)(NewsletterDetailView.as_view()), name='newsletter_detail'),
    path('newsletters/update/<str:slug>/', NewsletterUpdateView.as_view(), name='newsletter_update'),
    path('newsletters/delete/<str:slug>', NewsletterDeleteView.as_view(), name='newsletter_delete'),
    path('newsletters/attempts-report/', NewsletterAttemptsListView.as_view(), name='attempts_list'),
    path('newsletters/attempts-report/filter-newsletter/', NewsletterAttemptsListView.as_view(), name='attempts_list_filtered_newsletter'),
    path('newsletters/report/<int:pk>/', NewsletterAttemptsDetailView.as_view(), name='attempt_responses_detail')
]
