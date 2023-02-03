
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .form import InvoiceForm, ProductForm, ClientForm
from .models import Product, Client, Invoice
from django.contrib import messages


def dashboard_index(request):
    return render(request, "dashboard/dashboard_index.html")

# <--- PRODUCT --->


def product_detail(request, object_id):
    product = get_object_or_404(Product, pk=object_id)
    if request.method == "POST":
        product = ProductForm(data=request.POST, instance=product)
        if product.is_valid():
            messages.success(request, "El producto ha sido actualizado.")
            product.save()
            return redirect(to="product_list")

    context = {
        'form': form,
        "model_name": "Product"
    }
    form = ProductForm(instance=product)
    return render(request, 'dashboard/object_detail.html', context)


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
    model_name = "Product"

    context = {
        "model_name": model_name,
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
    context = {
        'form': form,
        "model_name": "Client"
    }
    form = ClientForm(instance=client)
    return render(request, 'dashboard/object_detail.html', context)


def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="client_list")
    else:
        form = ClientForm()

    return render(request, 'dashboard/object_detail.html', {'form': form, "model_name":"Client"})


def client_delete(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    messages.success(request, "Se elimino el producto.")
    client.delete()
    return redirect(to="client_list")


def client_list(request):
    object_list = Client.objects.all()
    model_name = "Client"

    context = {
        "model_name": model_name,
        "object_list": object_list
    }
    return render(request, 'dashboard/object_list.html', context)


# <---- INVOICES  ---->

def invoice_list(request):
    object_list = Invoice.objects.all()
    model_name = "Invoice"

    context = {
        "model_name": model_name,
        "object_list": object_list
    }
    return render(request, 'dashboard/object_list.html', context)


def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="invoice_list")
    else:
        form = InvoiceForm()

    return render(request, 'dashboard/object_detail.html', {'form': form, "model_name":"Invoice"})


def invoice_detail(request, object_id):
    invoice = get_object_or_404(Invoice, pk=object_id)

    if request.method == "POST":
        invoice = InvoiceForm(data=request.POST, instance=invoice)
        if invoice.is_valid():
            messages.success(request, "El producto ha sido actualizado.")
            invoice.save()
            return redirect(to="invoice_list")
    context = {
        'form': form,
        "model_name": "Invoice"
    }
    form = InvoiceForm(instance=invoice)
    return render(request, 'dashboard/object_detail.html', context)


def invoice_delete(request, client_id):
    invoice = get_object_or_404(Invoice, pk=client_id)
    messages.success(request, "Se elimino el producto.")
    invoice.delete()
    return redirect(to="invoice_list")
