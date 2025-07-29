from django.shortcuts import render

# Create your views here.

from django.contrib.auth.forms import UserCreationForm   # ユーザー登録用のフォームクラスをインポート
from django.urls import reverse_lazy
from django.views import generic
from .models import PurchaseHistory
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

# SignUpViewクラスを作成
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')     # サインアップ成功時、ログインページのURLにリダイレクト
    template_name = 'accounts/signup.html'

@login_required(login_url='login')  # ログインしてなかったらログインページにリダイレクト
def purchase_history(request):
    purchases = PurchaseHistory.objects.filter(user=request.user).order_by('-purchased_at')
    return render(request, 'accounts/purchase_history.html', {'purchases': purchases})