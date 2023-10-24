from .newsletter import NewsletterListView, NewsletterDetailView, NewsletterCreateView, NewsletterUpdateView, \
    NewsletterDeleteView
from .index import index
from .newsletter_attempt import NewsletterAttemptsListView, NewsletterAttemptsDetailView
from newsletter.views.regular_newsletters_manager import send_newsletter_manager, regular_newsletter_manager

__all__ = ['index', 'NewsletterListView', 'NewsletterDetailView', 'NewsletterCreateView', 'NewsletterUpdateView',
           'NewsletterDeleteView', 'NewsletterAttemptsListView', 'NewsletterAttemptsDetailView',
           'send_newsletter_manager', 'regular_newsletter_manager']
