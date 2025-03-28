from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('assortment/', views.assortment, name='assortment'),
    path('contacts', views.contacts, name='contacts'),
    path('basket', views.basket, name='basket'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('delete_to_cart/', views.delete_to_cart, name='delete_to_cart'),
    path('delete_to_cart_basket/', views.delete_to_cart_basket, name='delete_to_cart_basket'),
    # path('order', views.order_view, name='order'),
    path('success', views.success, name='success'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('is_basket/', views.is_basket, name='is_basket'),
    # path('update_db_plus/', views.update_cart, name='update_db_plus'),
]

