
from django import forms
from .models import Product, Client, Invoice
from django.utils import timezone


class InvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Invoice
        fields = ["iva", "subtotal", "total", "client"]
        widgets = {
            'iva': forms.TextInput(attrs={"class": "is_modified form-control", "type": "number"}),
            'due_at': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': timezone.now().strftime('%Y-%m-%d')
                }
            ),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,
            }),
            'total': forms.TextInput(attrs={
                'readonly': True,
            })
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "maker"]


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "email", "phone"]
