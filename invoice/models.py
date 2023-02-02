

# Create your models here.
from django.db import models
from django.utils import timezone
from django.db.models import (
    CharField, ForeignKey, DateTimeField, TextField, ManyToManyField)

STATUS = [("current", "activa"), ("paid", "pagado"),
          ("unpaid", "sin pagar"), ("expired", "vencida")]


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    maker = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Client(models.Model):
    name = CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    title = CharField(max_length=100)
    creation_at = DateTimeField(auto_now_add=True)
    due_at = DateTimeField(null=False, blank=True,
                           default=timezone.now() + timezone.timedelta(days=7))
    updated_at = DateTimeField(auto_now=True)
    status = CharField(
        choices=STATUS, default=STATUS[0][1], max_length=100)
    comment = TextField(null=False, blank=True)
    client = ForeignKey(Client, on_delete=models.CASCADE)
    products = ManyToManyField(Product)

    def __str__(self) -> str:
        return self.title
