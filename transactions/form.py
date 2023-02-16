
from django import forms
from .models import Transaccion, Tramite, Vehiculo


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

    name = forms.CharField(label="Nombre", widget=forms.TextInput(
        attrs={"class": "form-control", "type": "text", "required": True}))
    registro = forms.ChoiceField(label='Registro Nacional', choices=Tramite.RegistroNacional.choices, widget=forms.Select(
        attrs={"class": "custom-select d-block w-100 p-2"}))

    clasificacion = forms.ChoiceField(label='Tipo de Vehiculo', choices=Vehiculo.Clase.choices, widget=forms.Select(
        attrs={"class": "custom-select d-block w-100 p-2"}))

    vigencia = forms.DateField(label="Vigencia", widget=forms.DateInput(
        attrs={'type': 'date', "class": "form-control"}))
