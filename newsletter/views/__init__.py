from .newsletter import NewsletterListView, NewsletterDetailView, NewsletterCreateView, NewsletterUpdateView, \
    NewsletterDeleteView
from .index import index
from .newsletter_attempt import NewsletterAttemptsListView, NewsletterAttemptsDetailView

__all__ = ['index', 'NewsletterListView', 'NewsletterDetailView', 'NewsletterCreateView', 'NewsletterUpdateView',
           'NewsletterDeleteView', 'NewsletterAttemptsListView', 'NewsletterAttemptsDetailView']
