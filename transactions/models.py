

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core import serializers
import json
CLASSIFICATION = [
    ('automobile', 'automóvil'),
    ('motorcycle', 'moto')
]
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
]

NATIONAL_REGISTRY = [
    ("rna", "RNA"), ("rnc", "RNC")
]


class Vehiculo(models.Model):
    classification = models.CharField(max_length=30, choices=CLASSIFICATION, default=CLASSIFICATION[0][0])
    license_plate = models.CharField(max_length=100)

    def __str__(self):
        return self.classification + ' - ' + self.license_plate


class Cliente(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    document_type = models.CharField(max_length=100)
    document_number = models.IntegerField()
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ' ' + self.last_name


class Asesor(models.Model):
    name = models.CharField(max_length=100)
    employee_number = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ' - ' + self.employee_number


class Derecho(models.Model):
    name = models.CharField(max_length=100)
    classification = models.CharField(max_length=30, choices=CLASSIFICATION)
    percentage = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.name + ' - ' + self.classification


class Tramite(models.Model):
    name = models.CharField(max_length=100)
    national_register = models.CharField(
        choices=NATIONAL_REGISTRY, max_length=30)
    classification = models.CharField(
        choices=CLASSIFICATION, max_length=30, default=CLASSIFICATION[0][0])
    derechos = models.ManyToManyField(Derecho)
    vigencia = models.DateTimeField()

    def __str__(self):
        return self.name + ' - ' + self.classification

    def to_json(self):
        derechos = self.derechos
        data = serializers.serialize('json', [self])
        json_data = json.loads(data)[0]["fields"]
        json_data.update({"value": f"{self.name} - {self.classification}"})
        return json_data


class TramiteDerecho(models.Model):
    derecho = models.ForeignKey(Derecho, on_delete=models.CASCADE)
    tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE)
    sale_value = models.DecimalField(max_digits=15, decimal_places=2)
    vigencia = models.DateTimeField()


class Transaccion(models.Model):
    client = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    creation_at = models.DateTimeField(auto_now_add=True)
    vehicle = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )
    comment = models.TextField()
    national_register = models.CharField(
        choices=NATIONAL_REGISTRY, max_length=30)  # ¿Realmente debe ir este campo?

    def __str__(self):
        return self.status
