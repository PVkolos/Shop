from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('/create_payment/', views.create_payment, name='create_payment'),
    path('/success', views.success, name='success'),
    path('/order', views.order_view, name='order'),
]
