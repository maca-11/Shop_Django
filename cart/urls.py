from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('', views.cart_list, name='cart_list'),
    path('delete/', views.delete, name='delete'),
    path('purchase/selected/', views.checkout, name='checkout'),
    
]