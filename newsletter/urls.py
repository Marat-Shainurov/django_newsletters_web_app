from django.urls import path

from newsletter.apps import NewsletterConfig
from newsletter.views import NewsletterListView, NewsletterDetailView, NewsletterCreateView, NewsletterUpdateView, \
    NewsletterDeleteView, NewsletterAttemptsListView, NewsletterAttemptsDetailView, index, \
    regular_newsletter_manager, regular_newsletters_report, set_schedule, invalid_newsletter_settings

app_name = NewsletterConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('newsletters/', NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletters/create/', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newsletters/detail/<str:slug>/', NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('newsletters/update/<str:slug>/', NewsletterUpdateView.as_view(), name='newsletter_update'),
    path('newsletters/delete/<str:slug>', NewsletterDeleteView.as_view(), name='newsletter_delete'),
    path('newsletters/attempts-report/', NewsletterAttemptsListView.as_view(), name='attempts_list'),
    path('newsletters/reports/<int:pk>/', NewsletterAttemptsDetailView.as_view(), name='attempt_responses_detail'),
    path('newsletters/control-panel/', regular_newsletter_manager, name='control_panel'),
    path('newsletters/general-report/', regular_newsletters_report, name='regular_newsletters_report'),
    path('newsletters/schedule-settings/', set_schedule, name='set_schedule'),
    path('newsletters/control-panel/invalid-settings/<str:slug>/', invalid_newsletter_settings,
         name='invalid_newsletter_settings'),
]
