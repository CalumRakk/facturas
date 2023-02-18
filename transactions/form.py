
from django import forms
from .models import Transaccion, Tramite, Vehiculo, Cliente


class VehiculoForm(forms.ModelForm):    
    class Meta:
        model = Vehiculo
        fields = '__all__'
    
    tipo_vehiculo= forms.ChoiceField(label='Tipo de Vehiculo', choices=Vehiculo.Clase.choices, widget=forms.Select(
        attrs={"class": "form-select form-select-sm w-auto"}))

    placa= forms.CharField(max_length=20, label="Placa", widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"N. Placa "}))

class ClienteForm(forms.ModelForm):    
    class Meta:
        model = Cliente
        fields = '__all__'
    tipo_documento= forms.ChoiceField(label='T. Documento', choices=Cliente.TipoDocumento.choices, widget=forms.Select(
        attrs={"class": "form-select form-select-sm w-auto"}))
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