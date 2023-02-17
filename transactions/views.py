import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest, QueryDict
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from django.urls import reverse

from .models import Derecho, Tramite, Cliente, Transaccion, Vehiculo
from .form import TransaccionForm, TramiteForm, ClienteForm
from .serializers import TramiteSerializer, ClienteSerializer
from django.core.exceptions import ValidationError


def buscar_objeto(Modelo, id_objeto):
    try:
        objeto = Modelo.objects.get(id=id_objeto)
        return objeto
    except Modelo.DoesNotExist:
        return None

def test(request):
    if request.method == "GET":
        form = TramiteForm()
        return render(request, 'test.html', {"form": form})

    elif "buscar-cliente" == request.headers.get("X-Requested-Type"):
        """Devuelve un Array de Clientes.
        Nota: en el Ajax es donde se debe obtener el primer elemento del array. Esto es así, porque
        es más facil comprobar si se ha devuelto datos en un array que comprobar si el objeto tiene datos o está vacio.
        """
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

    elif "create_user" == request.headers.get("X-Requested-Type"):
        querydict = QueryDict(request.body)
        cliente = ClienteForm(querydict)
        if cliente.is_valid():
            cliente = cliente.save()
            serializer = ClienteSerializer(cliente)
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse([], safe=False)

    elif "procesar-transaccion" == request.headers.get("X-Requested-Type"):
        # Los datos de un modelo relacionado con Transacción deben enviarse deben ser un json (no un valor Id o otra cosa.)
        # Ejemplo : data = {"cliente": {"id":"1"}} En este caso el modelo cliente tiene un Json y un campo `id`.
        # Si el JSON del modelo contiene un campo `id` se da por hecho que el asesor selecciono y busco un objeto existente en la base de datos.
        # Si el JSON del modelo no contiene un campo `id` se da por hecho que el JSON tiene los campos necesarios para crear un objeto de ese modelo.
        custom_errors={}
        data = json.loads(request.body)
        
        cliente= None
        cliente_json= data.get('cliente')
        if cliente_json is None or not isinstance(cliente_json, dict):
            custom_errors.update({"cliente":"Cliente no está presente o no es un Json."})
        
        if cliente_json.get("id"):
            cliente= buscar_objeto(Cliente, cliente_json.get("id"))
        else:
            clienteForm = ClienteForm(data=cliente_json)
            if clienteForm.is_valid():
                cliente = clienteForm.save(commit=False)
            else:
                custom_errors.update({"cliente": clienteForm.errors.as_text() })

        if not isinstance(cliente, Cliente):
            custom_errors.update({"cliente":"No se pudo crear ni instanciar un cliente con los datos enviados"})

        if len(custom_errors.keys())>0:            
            return JsonResponse(custom_errors, safe=False)
        # En este punto ocurren dos cosas:
        # Los objetos relacionados con Transaccion tienen sus datos validaos
        # En caso que un objeto no tenga id es porque es un nuevo objeto que se debe guardar en DB antes de poder pasarselo a Transaccion.
        if cliente.pk is None:
            cliente.save()    
      
        data["cliente"]=cliente
        data["vehiculo"]= Vehiculo.objects.get(id=data["vehiculo"])
        data["tramite"]= Tramite.objects.get(id=data["tramite"])
        data["valor_total"]= "1"     

        transaction = TransaccionForm(data=data)
        if transaction.is_valid():
            transaction.save()
            return JsonResponse({"redirect_url": reverse("transactions:test")})
        return JsonResponse({'error': transaction.errors.as_text()}, status=400)       
        

    elif "pre-select" in request.POST:
        registro_name = 'registro'
        clasificacion_name = 'clasificacion'

        initial_data = {
            registro_name: request.POST.get(registro_name),
            clasificacion_name: request.POST.get(clasificacion_name)
        }

        tramite = TramiteForm(initial=initial_data)

        tramite.fields[registro_name].widget.attrs['disabled'] = True
        tramite.fields[clasificacion_name].widget.attrs['disabled'] = True
        transaccion = TransaccionForm()
        cliente = ClienteForm()
        return render(request, 'test-2.html', {"transaccion": transaccion, "tramite": tramite, "cliente": cliente})


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


class Tramite_view(View):
    def get(self, request):
        form = TramiteForm()
        return render(request, 'dashboard/test.html', {"form": form})

    def post(self, request):
        if request.headers.get("X-Requested-Type") == "autocomplete":
            json_data = json.loads(request.body.decode("utf-8"))

            products = Derecho.objects.filter(
                classification__icontains=json_data["classification"])
            response_json = []
            for product in products:
                response_json.append(
                    {
                        "id": product.pk,
                        "value": f"{product.name} - ${product.sale_value}",
                        "name": product.name,
                        "classification": product.classification,
                        "percentage": round(product.percentage),
                        "sale_value": product.sale_value
                    }
                )
            return JsonResponse(response_json, safe=False)

        elif request.headers.get("X-Requested-Type") == "post":
            # TODO: Si alguien hace una petición post enviando los datos adecuados, pero con id de Derechos no existente ¿que ocurre?
            data = json.loads(request.body)["tramite"]

            derechos_id: list = data["derechos"]
            derechosSer = DerechoSerializer(
                Derecho.objects.filter(id__in=derechos_id), many=True)
            data["derechos"] = derechosSer.data

            tramite = TramiteSerializer(Tramite, data=data)
            if tramite.is_valid():
                tramite.save()
                return JsonResponse({"redirect_url": reverse("transactions:tramite")})
        return HttpResponseBadRequest("Invalid request")
