

from django.contrib import admin
from .models import Tramite, Derecho, Cliente, Transaccion, Vehiculo

admin.site.register(Tramite)
admin.site.register(Derecho)
admin.site.register(Cliente)
admin.site.register(Transaccion)
admin.site.register(Vehiculo)