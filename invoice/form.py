
from django import forms
from .models import Transaccion, Tramite, NATIONAL_REGISTRY, CLASSIFICATION


class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ["status"]
    cliente = forms.CharField(widget=forms.TextInput)


class TramiteForm(forms.ModelForm):
    class Meta:
        model = Tramite
        fields =["name","national_register", "classification", "vigencia"]
    name = forms.CharField(label="Nombre", widget=forms.TextInput(
        attrs={"class": "form-control", "type": "text", "required": True}))
    national_register = forms.ChoiceField(label='Registro Nacional', choices=NATIONAL_REGISTRY, widget=forms.Select(
        attrs={"class": "custom-select d-block w-100 p-2"}))
    classification = forms.ChoiceField(label='Tipo de Vehiculo', choices=CLASSIFICATION, widget=forms.Select(
        attrs={"class": "custom-select d-block w-100 p-2"}))

    # derechos = forms.ChoiceField(widget=forms.Select(attrs={"style": "display:none;"}))
    # derechos = forms.CharField(label="derechos", widget=forms.TextInput(
    #     attrs={"type": "text", "placeholder": "Buscar derecho...", "style": "display:none;"}))

    vigencia = forms.DateField(label="Vigencia", widget=forms.DateInput(attrs={'type': 'date',"class": "form-control"}))
