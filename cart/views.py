from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, get_object_or_404
from shopsite.models import Product

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # カート追加ロジック
    return redirect('shopsite:detail', pk=pk)