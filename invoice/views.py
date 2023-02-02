
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .form import InvoiceForm, ProductForm
from .models import Product
from crispy_forms.helper import FormHelper
from django.contrib import messages

# def update_profile(request):
#     profile = request.user.profile
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = ProfileForm(instance=profile)
#     return render(request, 'update_profile.html', {'form': form})


def index(request):
    return render(request, "dashboard/dashboard_index.html")


def invoice_detail(request):
    form = InvoiceForm()
    return render(request, 'login.html', {'form': form})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == "POST":
        product = ProductForm(data=request.POST, instance=product)
        if product.is_valid():
            messages.success(request, "El producto ha sido actualizado.")
            product.save()
            return redirect(to="product_list")

    form = ProductForm(instance=product)
    return render(request, 'dashboard/product_detail.html', {'form': form})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="product_list")
    else:
        form = ProductForm()

    return render(request, 'dashboard/product_detail.html', {'form': form})


def product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    messages.success(request, "Se elimino el producto.")
    product.delete()
    return redirect(to="product_list")


def product_list(request):
    products = Product.objects.all()
    return render(request, 'dashboard/product_list.html', {'products': products})
