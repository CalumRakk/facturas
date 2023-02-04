

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
STATUS = [("current", "activa"), ("paid", "pagado"),
          ("unpaid", "sin pagar"), ("expired", "vencida")]


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    maker = models.CharField(max_length=100)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.pk} {self.name}"

class Invoice(models.Model):
    iva = models.IntegerField(default=16)
    subtotal = models.DecimalField(
        default=0.00, decimal_places=2, max_digits=8)
    total = models.DecimalField(default=0.00, decimal_places=2, max_digits=8)
    due_at = models.DateTimeField(null=False, blank=True,
                                  default=timezone.now() + timezone.timedelta(days=7))

    status = models.CharField(
        choices=STATUS, default=STATUS[0][1], max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=False, blank=True)

    creation_at = models.DateTimeField(auto_now_add=True)

    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class Product_Sale(models.Model):
    count_sale = models.IntegerField(default=0)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=8)
    subtotal = models.DecimalField(
        default=0.00, decimal_places=2, max_digits=8)

    sale = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
