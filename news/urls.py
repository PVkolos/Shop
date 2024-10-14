from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_home, name='news_home'),
    path('add_product/', views.add_product, name='add_product'),

]