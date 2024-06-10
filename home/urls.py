from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('faq/', views.faq, name='faq'),
    path('products/', include('products.urls')),
]
