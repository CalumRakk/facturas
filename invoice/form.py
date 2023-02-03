
from django import forms
from .models import Invoice, Product, Client


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ("__all__")
    due_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
