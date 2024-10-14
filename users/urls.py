from django.urls import path
from . import views

urlpatterns = [
    path('/register/', views.RegisterUser.as_view(), name='register'),
    path('/login/', views.LoginUser.as_view(), name='login'),
    path('/private', views.private_office, name='private')

]