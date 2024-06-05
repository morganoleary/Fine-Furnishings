from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('sofas/', views.sofa_products, name='sofa_products'),
    path('bedroom/', views.bedroom_products, name='bedroom_products'),
    path('dining/', views.dining_products, name='dining_products'),
]