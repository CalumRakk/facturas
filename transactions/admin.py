

from django.contrib import admin
from .models import Cliente, Vehiculo, Tramite, Derecho, TramiteDerecho, Transaccion


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "num_documento",
        "nombre",
        "apellido",
        "tipo_documento",
        "actualizado",
    )
    list_filter = ["actualizado"]
    search_fields = ("nombre", "apellido", "num_documento")


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("placa", "tipo_vehiculo", "cliente", "actualizado")
    list_filter = ["actualizado"]
    search_fields = ("placa", "cliente")


class DerechoInline(admin.TabularInline):
    model = TramiteDerecho
    fields = ("derecho", "valor")
    extra = 1


@admin.register(Tramite)
class TramiteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "registro", "clasificacion", "vigencia")
    list_filter = ["registro", "clasificacion"]
    search_fields = ("nombre", "vigencia")
    inlines = [DerechoInline]


@admin.register(Derecho)
class DerechoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo", "actualizado")
    list_filter = ["activo"]
    search_fields = ("nombre",)


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ("creado", "tramite", "cliente","vehiculo" )
    list_filter = ["creado"]
    search_fields = ("tramite", "vehiculo")
    fields = ("cliente", "vehiculo", "tramite", "estado")