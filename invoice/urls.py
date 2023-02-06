
from django.contrib.auth.decorators import login_required
from django.urls import path
from invoice import views
from invoice.views import Client_View

app_name = 'invoice'
urlpatterns = [
    path('register/', views.signup, name="signup"),
    path('signup/', views.signup),
    
    path('login/', views.signin, name="signin"),
    path('', login_required(views.dashboard_index), name="dashboard_index"),
    
    path('clients/<int:client_id>/', login_required(Client_View.as_view()), name='client-detail'),
    path('clients/', login_required(Client_View.as_view()), name='client-detail')
]
