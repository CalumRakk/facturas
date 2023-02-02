

from django.urls import path
from invoice import views

urlpatterns = [
    path('', views.index, name="index"),
    path('invoice/', views.invoice_detail),    
    path('products/', views.product_list, name="product_list"),    
    path('products/<int:product_id>/', views.product_detail, name="product_detail"),
    path('products/create/', views.product_create, name="product_create"),
    path('products/delete/<int:product_id>/', views.product_delete, name="product_delete"),
    

    path('clients/', views.product_list, name="clients"),
    path('invoices/', views.product_list, name="invoices")
]
