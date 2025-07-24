from django.urls import path
from . import views

app_name = 'cart'  # ← これが名前空間の正体！

urlpatterns = [
    path('<int:pk>/add/', views.add_to_cart, name='add'),
]