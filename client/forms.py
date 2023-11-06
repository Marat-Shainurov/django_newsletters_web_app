from django import forms

from client.models import Client, City


class ClientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'comments':
                self.fields[field_name] = forms.CharField(
                    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}))
            if field_name == 'city':
                self.fields[field_name] = forms.ModelChoiceField(
                    queryset=City.objects.all(), )
                self.fields[field_name].widget.attrs['class'] = 'form-control'
            if field_name == 'is_signed_up':
                self.fields[field_name] = forms.BooleanField(
                    required=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox-small'}), label='Is signed up')

    class Meta:
        model = Client
        exclude = ('is_active', 'user', 'slug')


class CityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = City
        fields = ('city',)
