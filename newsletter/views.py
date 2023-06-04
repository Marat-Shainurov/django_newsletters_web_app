from django.shortcuts import render
from django.views import generic

from newsletter.models import NewsletterSettings


class NewsletterListView(generic.ListView):
    model = NewsletterSettings
