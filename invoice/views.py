
# Create your views here.
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View

from .models import Client
from .form import ClientForm


def signout(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    return redirect('invoice:signin')


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
        return redirect("invoice:dashboard")
    if request.user.is_authenticated:
        return redirect("invoice:dashboard")
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
            return redirect(to="invoice:dashboard")

    form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'signin.html', context)


def dashboard(request):
    messages.add_message(request,messages.WARNING, "Página por implementar.")
    return render(request, "dashboard/dashboard.html")


def index(request):
    return render(request, "index.html")


class Client_View(View):
    def get(self, request):
        form = ClientForm()
        clients = Client.objects.filter(user_id=request.user.id)
        context = {"clients": clients, 'form': form}
        return render(request, 'dashboard/client.html', context)

    def post(self, request):
        form = ClientForm(request.POST)
        if form.is_valid():
            form_valid = form.save(commit=False)
            form_valid.user = request.user
            form_valid.save()
            return redirect(to="invoice:client-detail")
        return HttpResponseBadRequest("Invalid request")

    def put(self, request):
        if request.PUT.get("id"):
            client_id = request.PUT["id"]
            cliente = get_object_or_404(Client, id=client_id)
            form = ClientForm(request.PUT, instance=cliente)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'Cliente actualizado con éxito'})
            return JsonResponse({'errors': form.errors}, status=400)
        return HttpResponseBadRequest("Invalid request")

    def delete(self, request):
        user = request.user
        json_data = json.loads(request.body.decode("utf-8"))
        if json_data.get("id"):
            client_id = json_data["id"]
            client = get_object_or_404(Client, id=client_id, user=user)
            client.delete()
            messages.add_message(request, messages.SUCCESS,
                                 'Producto eliminado con éxito')
            return JsonResponse({'message': 'Cliente eliminado con éxito'})
        return JsonResponse("Invalid request", status=400)
