
from django import forms
from .models import Invoice, Product,Client
from crispy_forms.helper import FormHelper



class InvoiceForm(forms.ModelForm):
    due_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = Invoice
        fields = "__all__"


class ProductForm(forms.ModelForm):
    class Meta:
        model= Product
        fields = "__all__"
        
class ClientForm(forms.ModelForm):
    class Meta:
        model= Client
        fields = "__all__"
