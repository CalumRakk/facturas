
from django import forms
from .models import Transaccion, Tramite, NATIONAL_REGISTRY, CLASSIFICATION



class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = '__all__'

    name = forms.CharField(label="Nombre", widget=forms.TextInput(
        attrs={"class": "form-control", "type": "text", "required": True}))
    national_register = forms.ChoiceField(label='Registro Nacional', choices=NATIONAL_REGISTRY, widget=forms.Select(
        attrs={"class": "custom-select d-block w-100 p-2"}))

    classification = forms.ChoiceField(label='Tipo de Vehiculo', choices=CLASSIFICATION, widget=forms.Select(
        attrs={"class": "custom-select d-block w-100 p-2"}))
    
    vigencia = forms.DateField(label="Vigencia", widget=forms.DateInput(attrs={'type': 'date',"class": "form-control"}))
