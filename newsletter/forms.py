from django import forms

from client.models import Client, City
from newsletter.models import Newsletter


class NewsletterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'content':
                self.fields[field_name] = forms.CharField(
                    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '8'}))
            if field_name == 'newsletter_cities':
                self.fields[field_name] = forms.ModelMultipleChoiceField(
                    queryset=City.objects.all(),)
                self.fields[field_name].widget.attrs['class'] = 'form-control'
            if field_name == 'start_campaign' or field_name == 'finish_campaign':
                self.fields[field_name].widget = forms.DateTimeInput(
                    attrs={'class': 'form-control datetime', 'type': 'datetime-local'}
                )

    class Meta:
        model = Newsletter
        exclude = ('created', 'slug', 'is_active', 'newsletter_user', 'status',)
