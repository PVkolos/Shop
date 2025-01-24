from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('/register/', views.RegisterUser.as_view(), name='register'),
    path('/login/', views.LoginUser.as_view(), name='login'),
    path('/private', views.private_office, name='private'),
    path('/orders', views.orders, name='orders'),
    path('/logout/',  LogoutView.as_view(), name='logout')
]