from django import forms

from newsletter.models import Newsletter


class NewsletterForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        exclude = ('is_active', 'created', 'slug', 'status')