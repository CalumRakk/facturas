
# Create your views here.
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from django.urls import reverse
from rest_framework.decorators import api_view

from .models import Derecho, Tramite
from .form import TransaccionForm, TramiteForm
from .serializers import TramiteSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

@api_view(('GET',))
def tramites_endpoint(request):
    limit = int(request.GET.get('limit', 100))
    page = int(request.GET.get('page', 1))
    offset = (page - 1) * limit
    tramites = Tramite.objects.all()[offset:offset + limit]
    serializer = TramiteSerializer(tramites, many=True)
    data = {'data': serializer.data}
    return Response(data, template_name="test.html")

def test(request):
    if request.headers.get("X-Requested-Type") == "get":
        # FIXME: Si se crean muchos tramites se estarian devolviendo todos los de la base de datos. Limitar esto.
        tramites= Tramite.objects.all()
        return JsonResponse({"data":[tramite.to_json() for tramite in tramites]}, safe=False)
    if request.method == "POST":
        if request.headers.get("X-Requested-Type") == "autocomplete":
            json_data = json.loads(request.body.decode("utf-8"))

            products = Derecho.objects.filter(
                classification__icontains=json_data["classification"])
            response_json = []
            for product in products:
                response_json.append(
                    {
                        "id": product.pk,
                        "value": f"{product.name} - ${product.sale_value}" ,
                        "name": product.name,
                        "classification": product.classification,
                        "percentage": round(product.percentage),
                        "sale_value": product.sale_value
                    }
                )
            return JsonResponse(response_json, safe=False)

    form = TramiteForm()
    return render(request, "test.html", {"form": form})


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
        form = TransaccionForm()
        # clients = Client.objects.filter(user_id=request.user.id)
        # context = {"clients": clients, 'form': form}
        return render(request, 'dashboard/transaccion.html', {"form": form})


class Tramite_view(View):

    def get(self, request):
        form = TramiteForm()
        return render(request, 'dashboard/tramite.html', {"form": form})
    
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
                        "value": f"{product.name} - ${product.sale_value}" ,
                        "name": product.name,
                        "classification": product.classification,
                        "percentage": round(product.percentage),
                        "sale_value": product.sale_value
                    }
                )
            return JsonResponse(response_json, safe=False)
        
        elif request.headers.get("X-Requested-Type") == "post":
            # TODO: Si alguien hace una petición post enviando los datos adecuados, pero con id de Derechos no existente ¿que ocurre?
            data= json.loads(request.body)
            serializer = TramiteSerializer(data=data["data"])
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"redirect_url": reverse("transactions:tramite")})                   
        return HttpResponseBadRequest("Invalid request")
