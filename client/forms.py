from django import forms

from client.models import Client


class ClientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'is_signed_up':
                self.fields[field_name] = forms.BooleanField(
                    required=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox-small'}), label=field_name
                )

    class Meta:
        model = Client
        exclude = ('is_active', 'client_user')
