

# Create your models here.
from django.db import models
from django.utils import timezone
from django.db.models import Sum


class Cliente(models.Model):
    class TipoDocumento(models.TextChoices):
        CC = "CC", "Cedula de Ciudadania"
        CE = "CE", "Cedula de Extranjeria"
        TI = "TI", "Tarjeta de Identidad"
        RC = "RC", "Registro Civil"
        PA = "PA", "Pasaporte"

    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    tipo_documento = models.CharField(
        max_length=2, choices=TipoDocumento.choices, default=TipoDocumento.CC
    )
    num_documento = models.CharField(max_length=20, unique=True, db_index=True)
    telefono = models.CharField(max_length=20, blank=True)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.apellido = self.apellido.upper()
        super(Cliente, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre.capitalize()} {self.apellido.capitalize()} - {self.tipo_documento}{self.num_documento}"


class Vehiculo(models.Model):
    class Clase(models.TextChoices):
        MOTO = "MOTO", "Moto"
        AUTOMOVIL = "AUTOMOVIL", "Automovil"
        MOTOCARRO = "MOTOCARRO", "Motocarro"

    tipo_vehiculo = models.CharField(
        max_length=50, choices=Clase.choices, default=Clase.AUTOMOVIL
    )
    placa = models.CharField(max_length=20, unique=True, db_index=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.placa = self.placa.upper()
        super(Vehiculo, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.placa.upper()} - {self.tipo_vehiculo}"


class Derecho(models.Model):
    nombre = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Derecho, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre.upper()}"


class Tramite(models.Model):
    class RegistroNacional(models.TextChoices):
        RNA = "RNA", "Registro Nacional de Automotores"
        RNC = "RNC", "Registro Nacional de Conductor"

    nombre = models.CharField(max_length=200)

    registro = models.CharField(
        max_length=3, choices=RegistroNacional.choices, default=RegistroNacional.RNA
    )

    clasificacion = models.CharField(
        max_length=50, choices=Vehiculo.Clase.choices, default=Vehiculo.Clase.AUTOMOVIL
    )

    vigencia = models.DateField()

    derechos = models.ManyToManyField(
        Derecho, through="TramiteDerecho", related_name="derechos"
    )

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Tramite, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.registro} : {self.clasificacion} : {self.nombre.upper()}"


class TramiteDerecho(models.Model):
    tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE)
    derecho = models.ForeignKey(Derecho, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=0)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.tramite} : {self.derecho} : {self.valor}"


class Transaccion(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        PAGADO = "PAGADO", "Pagado"
        CANCELADO = "CANCELADO", "Cancelado"


    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE)

    estado = models.CharField(
        max_length=10, choices=Estado.choices, default=Estado.PENDIENTE
    )

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.cliente} : {self.vehiculo} : {self.tramite} : {self.estado}"
    
    valor_total = models.DecimalField(max_digits=10, decimal_places=0, default=0.00) # No parece necesario tener este campo.

    def save(self, *args, **kwargs):
        self.valor_total = self.tramite.tramitederecho_set.aggregate(Sum("valor"))["valor__sum"]
        super(Transaccion, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("transaccion_detail", kwargs={"pk": self.pk})
