from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'), # サインアップページ
    path('purchase_history/', views.purchase_history, name='history'),
]