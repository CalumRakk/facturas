
from django import forms
from .models import Transaccion, Tramite, Vehiculo, Cliente


class ClienteForm(forms.ModelForm):    
    class Meta:
        model = Cliente
        fields = '__all__'
class TramiteForm(forms.ModelForm):
    class Meta:
        model = Tramite
        fields = '__all__'

    registro = forms.ChoiceField(label='Registro Nacional', choices=Tramite.RegistroNacional.choices, widget=forms.Select(
        attrs={"class": "custom-select d-block w-100 p-2"}))
    clasificacion = forms.ChoiceField(label='Tipo de Vehiculo', choices=Vehiculo.Clase.choices, widget=forms.Select(
        attrs={"class": "custom-select d-block w-100 p-2"}))


class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = '__all__'

    def clean(self):
        
        cleaned_data = super().clean()
        # mi_campo_valor = cleaned_data.get('mi_campo')
        # cleaned_data['mi_campo'] = mi_campo_valor.upper()
        return cleaned_data