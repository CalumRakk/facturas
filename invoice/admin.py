from django.contrib import admin
from .models import Invoice,Client,Product
# Register your models here.
admin.site.register(Invoice)
admin.site.register(Client)
admin.site.register(Product)