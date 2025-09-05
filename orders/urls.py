from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.orders, name='index'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]
