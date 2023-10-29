from .newsletter import NewsletterListView, NewsletterDetailView, NewsletterCreateView, NewsletterUpdateView, \
    NewsletterDeleteView
from .index import index
from .newsletter_attempt import NewsletterAttemptsListView, NewsletterAttemptsDetailView
from .regular_newsletters_manager import (regular_newsletter_manager, regular_newsletters_report)
from .set_schedule import set_schedule

__all__ = ['index', 'NewsletterListView', 'NewsletterDetailView', 'NewsletterCreateView', 'NewsletterUpdateView',
           'NewsletterDeleteView', 'NewsletterAttemptsListView', 'NewsletterAttemptsDetailView',
           'regular_newsletter_manager', 'regular_newsletters_report',
           'set_schedule']
