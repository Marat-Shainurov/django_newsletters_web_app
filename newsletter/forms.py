from django import forms

from newsletter.models import Newsletter


class NewsletterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Newsletter
        exclude = ('created', 'slug', 'is_active', 'newsletter_user')
