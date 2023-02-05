
# Create your views here.
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse

from .serializers import InvoiceSerializer

from .models import Product, Client, Invoice, Product_Sale
from .form import ProductForm, ClientForm, InvoiceForm


def signup(request: HttpRequest):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        # if form.is_valid():
        #     user= form.save()
        #     login(request, user )
        #     return redirect('dashboard_index')
        # FIXME: REGISTRA USUARIO SIN VALIDAR CASI NADA
        username = request.POST["username"]
        password = request.POST["password1"]
        user = User.objects.create_user(
            username=username,
            password=password)
        user.save()
        login(request, user)
        return redirect("/")
    if request.user.is_authenticated:
        return redirect('dashboard_index')

    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'signup.html', context)


def dashboard_index(request):
    return render(request, "dashboard/dashboard-index.html")

# <--- PRODUCT --->


# def product_detail(request, object_id):
#     product = get_object_or_404(Product, pk=object_id)
#     if request.method == "POST":
#         product = ProductForm(data=request.POST, instance=product)
#         if product.is_valid():
#             messages.success(request, "El producto ha sido actualizado.")
#             product.save()
#             return redirect(to="product_list")

#     form = ProductForm(instance=product)
#     context = {
#         'form': form,
#         "model_name": "Product"
#     }
#     return render(request, 'dashboard/object_detail.html', context)

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form_valid = form.save(commit=False)
            form_valid.user = request.user
            form_valid.save()
            return redirect(to="product_list")
    else:
        form = ProductForm()
    return render(request, 'dashboard/product-create.html', {'form': form})


@login_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    messages.success(request, "Se elimino el producto.")
    product.delete()
    return redirect(to="product_list")


@login_required
def product_list(request):
    products = Product.objects.filter(user_id=request.user.id)
    return render(request, 'dashboard/products.html', {"products": products})


# <---- CLIENTS  ---->

# @login_required
# def client_detail(request, object_id):
#     client = get_object_or_404(Client, pk=object_id)
#     if request.method == "POST":
#         client = ClientForm(data=request.POST, instance=client)
#         if client.is_valid():
#             messages.success(request, "El producto ha sido actualizado.")
#             client.save()
#             return redirect(to="client_list")

#     form = ClientForm(instance=client)
#     context = {
#         'form': form,
#         "model_name": "Client"
#     }

#     return render(request, 'dashboard/object_detail.html', context)

@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            print(request.POST)
            form_valid = form.save(commit=False)
            form_valid.user = request.user
            form_valid.save()
            return redirect(to="client_list")
    else:
        form = ClientForm()

    return render(request, 'dashboard/client-create.html', {'form': form})


@login_required
def client_delete(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    messages.success(request, "Se elimino el producto.")
    client.delete()
    return redirect(to="client_list")


@login_required
def client_list(request):
    object_list = Client.objects.filter(user_id=request.user.id)
    model_name = "Client"

    context = {
        "model_name": model_name,
        "object_list": object_list
    }
    return render(request, 'dashboard/clients.html', context)


# <---- INVOICES  ---->
@login_required
def invoice_list(request):
    invoices = Invoice.objects.filter(client_id=request.user.id)
    return render(request, 'dashboard/invoices.html', {"invoices": invoices})


@login_required
def invoice_create(request):
    if request.method == 'POST':
        if request.headers.get("X-Requested-Type") == "autocomplete":
            user = request.user
            json_data = json.loads(request.body.decode("utf-8"))
            
            products = Product.objects.filter(
                user_id=user.id, name__icontains=json_data["query"])
            response_json = []
            for product in products:
                response_json.append(
                    {
                        "name": product.name,
                        "value": product.name,
                        "id": product.pk,
                        "price": product.price,
                        "maker": product.maker
                    }
                )
            return JsonResponse(response_json, safe=False)
        # if request.headers.get("X-Requested-Type") == "invoice_create":
        #     data = json.loads(request.body.decode("utf-8"))
        #     serializer = InvoiceSerializer(data=data)
        #     if serializer.is_valid():
        #         # TODO: el error de serializer.validate_product_ids no lo estoy manejando.
        #         product_ids= data["products"]
        #         serializer.validate_product_ids(product_ids, user=request.user)

        #         product_ids = [pk if isinstance(pk, int) else int(pk)
        #                 for pk in product_ids]

        #         products = Product.objects.filter(pk__in=product_ids, user_id=user.id)
        #         messages.success(request, "Añadido Factura")
        #         serializer.save()
        #         return JsonResponse({"redirect_url": reverse("invoice_list")})
            
        #     return JsonResponse(serializer.errors)
    else:
        clients = Client.objects.filter(user_id=request.user)
        products = Product.objects.filter(user_id=request.user.id)
        form = InvoiceForm(clients=clients)
    return render(request, 'dashboard/invoice-create.html', {'form': form, "products": products})


# def invoice_detail(request, object_id):
#     invoice = get_object_or_404(Invoice, pk=object_id)

#     if request.method == "POST":
#         invoice = InvoiceForm(data=request.POST, instance=invoice)
#         if invoice.is_valid():
#             messages.success(request, "El producto ha sido actualizado.")
#             invoice.save()
#             return redirect(to="invoice_list")
#     form = InvoiceForm(instance=invoice)
#     context = {
#         'form': form,
#         "model_name": "Invoice"
#     }
#     return render(request, 'dashboard/object_detail.html', context)


def invoice_delete(request, client_id):
    invoice = get_object_or_404(Invoice, pk=client_id)
    messages.success(request, "Se elimino el producto.")
    invoice.delete()
    return redirect(to="invoice_list")
