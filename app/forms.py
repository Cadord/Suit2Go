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


class CheckoutEnderecoForm(forms.Form):
    endereco_rua = forms.CharField(label="Rua", required=True)
    endereco_numero = forms.CharField(label="Número", required=True)
    endereco_bairro = forms.CharField(label="Bairro", required=True)
    endereco_cidade = forms.CharField(label="Cidade", required=True)
    endereco_cep = forms.CharField(label="CEP", required=True)
    endereco_complemento = forms.CharField(label="Complemento")

class CheckoutDataForm(forms.Form):
    data_inicio = forms.DateTimeField(label="Para quando deseja agendar a entrega?", required=True, widget=forms.DateInput(
        attrs={'type': 'date', 'placeholder': "DD/MM/YYYY", 'class': 'form-control'}
    ))
    data_termino = forms.DateTimeField(label="Para quando deseja agendar a devolução?", required=True, widget=forms.DateInput(
        attrs={'type': 'date', 'placeholder': "DD/MM/YYYY", 'class': 'form-control'}
    ))