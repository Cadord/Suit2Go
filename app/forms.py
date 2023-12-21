from django import forms
from .models import Roupas
class RoupasForms(forms.ModelForm):
    class Meta:
        model = Roupas
        fields = '__all__'