
from django.contrib.auth.decorators import login_required
from django.urls import path
from invoice import views
from invoice.views import Transaccion_view, Tramite_view

app_name = 'invoice'
urlpatterns = [
    path('register/', views.signup, name="signup"),
    path('signup/', views.signup),
    path('login/', views.signin, name="signin"),
    path('', views.index, name="index"),
    path('signout/', views.signout, name="signout"),
    path('test/', views.test, name="test"),

    path('dashboard/', login_required(views.dashboard), name="dashboard"),
    path('tramite/', login_required(Tramite_view.as_view()), name='tramite')

]
