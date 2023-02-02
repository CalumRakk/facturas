
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .form import InvoiceForm, ProductForm, ClientForm
from .models import Product, Client
from django.contrib import messages


def index(request):
    return render(request, "dashboard/dashboard_index.html")


def invoice_detail(request):
    form = InvoiceForm()
    return render(request, 'login.html', {'form': form})

# <--- PRODUCT --->


def product_detail(request, object_id):
    product = get_object_or_404(Product, pk=object_id)

    if request.method == "POST":
        product = ProductForm(data=request.POST, instance=product)
        if product.is_valid():
            messages.success(request, "El producto ha sido actualizado.")
            product.save()
            return redirect(to="product_list")

    form = ProductForm(instance=product)
    return render(request, 'dashboard/object_detail.html', {'form': form})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="product_list")
    else:
        form = ProductForm()

    return render(request, 'dashboard/object_detail.html', {'form': form})


def product_delete(request, object_id):
    product = get_object_or_404(Product, pk=object_id)
    messages.success(request, "Se elimino el producto.")
    product.delete()
    return redirect(to="product_list")


def product_list(request):
    object_list = Product.objects.all()
    model_name = "Producto"
    url_name = "product_detail"

    context = {
        "model_name": model_name,
        "url_name": url_name,
        "object_list": object_list
    }
    return render(request, 'dashboard/object_list.html', context)

# <---- CLIENTS  ---->


def client_detail(request, object_id):
    client = get_object_or_404(Client, pk=object_id)

    if request.method == "POST":
        client = ClientForm(data=request.POST, instance=client)
        if client.is_valid():
            messages.success(request, "El producto ha sido actualizado.")
            client.save()
            return redirect(to="client_list")

    form = ClientForm(instance=client)
    return render(request, 'dashboard/object_detail.html', {'form': form})


def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="client_list")
    else:
        form = ClientForm()

    return render(request, 'dashboard/object_detail.html', {'form': form})


def client_delete(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    messages.success(request, "Se elimino el producto.")
    client.delete()
    return redirect(to="client_list")


def client_list(request):
    object_list = Client.objects.all()
    model_name = "Cliente"       
    url_name = "client_detail"

    context = {
        "model_name": model_name,
        "url_name": url_name,
        "object_list": object_list
    }
    return render(request, 'dashboard/object_list.html', context)
