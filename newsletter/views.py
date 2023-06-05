from django.shortcuts import render
from django.views import generic

from newsletter.models import Newsletter


class NewsletterListView(generic.ListView):
    model = Newsletter
