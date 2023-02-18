import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from django.urls import reverse

from .models import Tramite, Cliente, Vehiculo
from .form import TransaccionForm, TramiteForm, ClienteForm, VehiculoForm
from .utils import checker, buscar_objeto, search_in_model


def test(request):
    return JsonResponse([], safe=False)


def signout(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    return redirect('transactions:signin')


def signup(request: HttpRequest):
    if request.method == 'POST':
        # FIXME: MEJORAR LA CREACIÓN DE USUARIO.
        username = request.POST["username"]
        password = request.POST["password1"]
        user = User.objects.create_user(
            username=username,
            password=password)
        user.save()
        login(request, user)
        return redirect("transactions:dashboard")
    if request.user.is_authenticated:
        return redirect("transactions:dashboard")
    form = UserCreationForm
    context = {'form': form}
    return render(request, 'signup.html', context)


def signin(request: HttpRequest):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(to="transactions:dashboard")

    form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'signin.html', context)


def dashboard(request):
    messages.add_message(request, messages.WARNING, "Página por implementar.")
    return render(request, "dashboard/base.html")


def index(request):
    return render(request, "index.html")


class Transaccion_view(View):
    def get(self, request):
        tramite = TramiteForm()       
        cliente = ClienteForm()
        vehiculo= VehiculoForm()
        transaccion = TransaccionForm()
        context={
            "transaccion": transaccion, 
            "tramite": tramite, 
            "cliente": cliente,
            "vehiculo":vehiculo
        }
        return render(request, 'dashboard/transaccion.html', context)

    def post(self, request):
        if "buscar-cliente" == request.headers.get("X-Requested-Type"):
            json_data = json.loads(request.body.decode("utf-8"))

            num_documento_keyName = "num_documento"
            tipo_documento_keyName = "tipo_documento"

            is_num_documento_exists = True if json_data.get(
                num_documento_keyName) else False
            is_tipo_documento_exists = True if json_data.get(
                tipo_documento_keyName) else False

            if is_num_documento_exists and is_tipo_documento_exists:
                num_documento = json_data[num_documento_keyName]
                tipo_documento = json_data[tipo_documento_keyName]

                if num_documento.isnumeric():
                    clientes = Cliente.objects.filter(
                        num_documento=num_documento, tipo_documento=tipo_documento)
                    return JsonResponse(list(clientes.values()), safe=False)
            return JsonResponse([], safe=False)
        
        elif "buscar-vehiculo" == request.headers.get("X-Requested-Type"):
            json_data = json.loads(request.body.decode("utf-8"))
            fields=["tipo_vehiculo", "placa"]
            vehiculo= search_in_model(json_data, fields, Vehiculo)
            return JsonResponse(vehiculo, safe=False)

        elif "procesar-transaccion" == request.headers.get("X-Requested-Type"):
            # FIXME: añadir un limitar de cuantos transsaciones puede hacer un cliente.
            errors={}
            data = json.loads(request.body)
            
            cliente= checker(data, ClienteForm)        
            if isinstance(cliente, dict):
                errors.update(cliente)
            
            if len(errors.keys())  >0:  
                errors.update({"status":"fail"})          
                return JsonResponse(errors, safe=False)        
            
            if cliente.pk is None:
                cliente.save()  
        
            data["cliente"]=cliente
            data["vehiculo"]= buscar_objeto(Vehiculo, data.get("vehiculo"))
            data["tramite"]= buscar_objeto(Tramite, data.get("tramite"))
            data["valor_total"]= "1"     

            transaction = TransaccionForm(data=data)
            if transaction.is_valid():
                transaction.save()
                return JsonResponse({"status":"ok","redirect_url": reverse("transactions:test")})
            errors.update({"transaccion": transaction.errors.as_text(),"status":"fail"})
            return JsonResponse(errors, safe=False)       
            
        return JsonResponse({'status':'false'}, status=400)