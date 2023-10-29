from django.urls import path
from django.views.decorators.cache import cache_page

from newsletter.apps import NewsletterConfig
from newsletter.views import NewsletterListView, NewsletterDetailView, NewsletterCreateView, NewsletterUpdateView, \
    NewsletterDeleteView, NewsletterAttemptsListView, NewsletterAttemptsDetailView, index, \
    regular_newsletter_manager, regular_newsletters_report

app_name = NewsletterConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('newsletters/', NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletters/create/', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newsletters/detail/<str:slug>/', NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('newsletters/update/<str:slug>/', NewsletterUpdateView.as_view(), name='newsletter_update'),
    path('newsletters/delete/<str:slug>', NewsletterDeleteView.as_view(), name='newsletter_delete'),
    path('newsletters/attempts-report/', NewsletterAttemptsListView.as_view(), name='attempts_list'),
    path('newsletters/attempts-report/filter-newsletter/', NewsletterAttemptsListView.as_view(),
         name='attempts_list_filtered_newsletter'),
    path('newsletters/reports/<int:pk>/', NewsletterAttemptsDetailView.as_view(), name='attempt_responses_detail'),
    path('newsletters/newsletters-panel/', regular_newsletter_manager, name='regular_newsletter_manager'),
    path('newsletters/regular-newsletters-report/', regular_newsletters_report, name='regular_newsletters_report'),
]

# todo:
#  filters for 'managers' (clients and newsletters list, reports) or checkboxes for clients list???
#  Fixture
#  Readme
#  Docker-VM?
