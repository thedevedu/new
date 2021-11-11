from django.forms import ModelForm
from .models import Network

class NetworkForm(ModelForm):
    class Meta:
        model = Network
        fields = ['title', 'languages', 'description']

    def __init__(self, *args, **kwargs):
        super(NetworkForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            