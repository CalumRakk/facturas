
from django.contrib.auth.decorators import login_required
from django.urls import path
from invoice import views
from invoice.views import Client_View

app_name = 'invoice'
urlpatterns = [
    path('register/', views.signup, name="signup"),
    path('signup/', views.signup),    
    path('login/', views.signin, name="signin"),
    path('', views.index, name="index"),
    path('signout/', views.signout, name="signout"),

    path('dashboard/', login_required(views.dashboard), name="dashboard"),    
    path('clients/<int:client_id>/', login_required(Client_View.as_view()), name='client-detail'),
    path('clients/', login_required(Client_View.as_view()), name='client-detail')
]
