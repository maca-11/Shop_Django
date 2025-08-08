from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import SearchForm       # forms.pyからsearchFormクラスをインポート
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin   # LoginRequiredMixinをインポート
from django.core.exceptions import PermissionDenied 
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Category
from accounts.models import PurchaseHistory
from django.contrib import messages

# Create your views here.
from django.views import generic    # 汎用ビューのインポート

def index(request):
    products = Product.objects.all()
    return render(request, 'shopsite/index.html', {'products': products})

# DetailViewクラスを作成
class DetailView(generic.DetailView):
    model = Product
    template_name = 'shopsite/detail.html'
    
# CreateViewクラスを作成
class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Product
    template_name = 'shopsite/create.html'
    fields = ['category', 'name', 'description', 'price', 'stock']
    success_url = reverse_lazy('shopsite:index')  # 一覧ページに戻る
    # 格納する値をチェック
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)
    
class AddCategory(LoginRequiredMixin, generic.edit.CreateView):
    model = Category
    template_name = 'shopsite/add_category.html'
    fields = ['name']
    success_url = reverse_lazy('shopsite:add_category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


# UpdateViewクラスを作成
class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Product
    template_name = 'shopsite/create.html'
    fields = '__all__'
    success_url = reverse_lazy('shopsite:index')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user and not request.user.is_superuser:
            raise PermissionDenied  # ← 管理者以外なら403
        return super().dispatch(request, *args, **kwargs)


class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Product
    template_name = 'shopsite/delete.html'
    success_url = reverse_lazy('shopsite:index')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user and not request.user.is_superuser:
            raise PermissionDenied  # ← 管理者以外なら403
        return super().dispatch(request, *args, **kwargs)
    

# 検索機能のビュー
def search(request):
    searchform = SearchForm(request.GET)
    products = Product.objects.none()
    query = ''

    if searchform.is_valid():
        query = searchform.cleaned_data['words']
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    return render(request, 'shopsite/results.html', {
        'products': products,
        'searchform': searchform,
        'query': query
    })
    
# views.py の例
from django.shortcuts import redirect

def custom_login_redirect(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    else:
        return redirect('user_dashboard')
    
# カスタム403のビュー(アクセス権限が無い場合)
def custom_permission_denied_view(request, exception):
    return render(request, '403.html', {'error_message': str(exception)}, status=403)
    
@login_required
def buy_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.stock >= 1:
        # 在庫を減らす
        product.stock -= 1
        product.save()

        # 購入履歴に保存
        PurchaseHistory.objects.create(
            user=request.user,
            product=product,
            quantity=1  # 数量指定するなら変更OK
        )

        # 成功メッセージ
        messages.success(request, "ご購入ありがとうございました！")
    else:
        messages.warning(request, "申し訳ありません、在庫切れです。")

    return redirect('shopsite:detail', pk=pk)

from django.db.models import Count

@login_required
def recommend_view(request):
    # あなたへのおすすめ（購入履歴ベース）
    categories = Product.objects.filter(
        purchasehistory__user=request.user
    ).values_list('category', flat=True).distinct()

    recommended = Product.objects.filter(category__in=categories).exclude(
        purchasehistory__user=request.user
    ).distinct()[:5]

    # 全体のおすすめ（購入数が多い順）
    popular = Product.objects.annotate(
        purchase_count=Count('purchasehistory')
    ).order_by('-purchase_count')[:5]

    # その他の商品（おすすめに含まれていないもの）
    excluded_ids = list(recommended.values_list('id', flat=True)) + list(popular.values_list('id', flat=True))
    others = Product.objects.exclude(id__in=excluded_ids)

    return render(request, 'shopsite/recommend.html', {
        'recommended': recommended,
        'popular': popular,
        'others': others
    })