

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    vehicle_type = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=100)

    def __str__(self):
        return self.vehicle_type + ' - ' + self.license_plate


class Cliente(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    document_type = models.CharField(max_length=100)
    document_number = models.CharField(max_length=100)
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
    sale_value = models.DecimalField(max_digits=15, decimal_places=2)


class Tramite(models.Model):
    name = models.CharField(max_length=100)
    national_register = models.CharField(choices=NATIONAL_REGISTRY, max_length=30)
    classification = models.CharField(choices=CLASSIFICATION, max_length=30)
    derechos = models.ManyToManyField(Derecho)
    vigencia = models.DateTimeField()


class Transaccion(models.Model):
    assessor = models.ForeignKey(Asesor, on_delete=models.CASCADE)
    creation_at = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )
    comment = models.TextField()

    def __str__(self):
        return self.status
