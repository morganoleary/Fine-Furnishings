from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout/confirmation/<str:order_number>/', views.order_confirmation, name='order_confirmation'),
    path('api/get_address/<int:address_id>/', views.get_address, name='get_address'),
]
