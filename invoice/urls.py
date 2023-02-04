

from django.urls import path
from invoice import views


urlpatterns = [
    path('login/', views.register_view, name="dashboard_index"),
    path('', views.dashboard_index, name="dashboard_index"),
    
    path('products/', views.product_list, name="product_list"),    
    # path('products/<int:object_id>/', views.product_detail, name="product_detail"),
    path('products/create/', views.product_create, name="product_create"),
    path('products/delete/<int:product_id>/', views.product_delete, name="product_delete"),
    
    path('clients/', views.client_list, name="client_list"), 
    # path('clients/<int:object_id>/', views.client_detail, name="client_detail"),
    path('clients/create/', views.client_create, name="client_create"),
    path('clients/delete/<int:client_id>/', views.client_delete, name="client_delete"),

    
    path('invoices/', views.invoice_list, name="invoice_list"), 
    # path('invoices/<int:object_id>/', views.invoice_detail, name="invoice_detail"),
    path('invoices/create/', views.invoice_create, name="invoice_create"),
    path('invoices/delete/<int:object_id>/', views.invoice_delete, name="invoice_delete"),    
]
