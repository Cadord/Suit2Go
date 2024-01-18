from django import forms
from .models import Roupas
class RoupasForms(forms.ModelForm):
    class Meta:
        model = Roupas
        fields = '__all__'

class DateForm(forms.Form):
    date_1 = forms.DateField(label='Para quando deseja agendar a entrega? ', required=True)
    time_1 = forms.TimeField(label='Para que horas deseja agendar? ')
    endereco = forms.CharField(label='Digite o endereço para entrega')