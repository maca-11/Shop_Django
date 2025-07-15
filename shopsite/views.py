from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import SearchForm       # forms.pyからsearchFormクラスをインポート
from django.db.models import Q


# Create your views here.
from django.views import generic    # 汎用ビューのインポート
from .models import Product     # models.pyのArticleクラスをインポート

def index(request):
    products = Product.objects.all()
    return render(request, 'shopsite/index.html', {'products': products})

# DetailViewクラスを作成
class DetailView(generic.DetailView):
    model = Product
    template_name = 'shopsite/detail.html'
    
# CreateViewクラスを作成
class CreateView(generic.CreateView):
    model = Product
    template_name = 'shopsite/create.html'
    fields = '__all__'
    success_url = reverse_lazy('shopsite:index')  # 一覧ページに戻る

# UpdateViewクラスを作成
class UpdateView(generic.UpdateView):
    model = Product
    template_name = 'shopsite/create.html'
    fields = '__all__'
    success_url = reverse_lazy('shopsite:index')  # 一覧ページに戻る

class DeleteView(generic.DeleteView):
    model = Product
    template_name = 'shopsite/delete.html'
    success_url = reverse_lazy('shopsite:index')
    

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