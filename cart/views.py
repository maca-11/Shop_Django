from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from shopsite.models import Product
from .models import CartItem
from django.contrib import messages
from accounts.models import PurchaseHistory  # 忘れずインポート！



@login_required
def cart_list(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum([item.product.price * item.quantity for item in items])
    return render(request, 'cart/list.html', {'items': items, 'total': total})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if product.stock < 1:
        messages.warning(request, "在庫切れのためカートに追加できません。")
        return redirect('shopsite:detail', pk=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "カートに追加しました！")
    return redirect('shopsite:detail', pk=product_id)


@login_required
def checkout(request):
    if request.POST.get("action") == 'purchase':
        selected_ids = request.POST.getlist('selected_items')
        purchased_items = []
        total = 0

        items = CartItem.objects.filter(user=request.user, id__in=selected_ids)  # ← 選択された商品だけ対象

        for item in items:
            product = item.product
            if product.stock < item.quantity:
                messages.error(request, f"{product.name} の在庫が足りません。")
                return redirect('cart:cart_list')

            total += product.price * item.quantity
            purchased_items.append({
                'name': product.name,
                'quantity': item.quantity,
                'price': product.price
            })

            # ✅ 履歴に保存
            from accounts.models import PurchaseHistory
            PurchaseHistory.objects.create(
                user=request.user,
                product=product,
                quantity=item.quantity
            )

            product.stock -= item.quantity
            product.save()
            item.delete()

        return render(request, 'cart/purchase_complete.html', {
            'purchased_items': purchased_items,
            'total': total
        })
    else:
        return redirect('cart:cart_list')  # GETアクセス時は一覧に戻す
    
@login_required
def delete(request):
    action = request.POST.get("action")
    selected_ids = request.POST.getlist('selected_items')

    if action == "delete":
        if not selected_ids:
            messages.warning(request, "削除する商品が選択されていません。")
        else:
            CartItem.objects.filter(user=request.user, id__in=selected_ids).delete()
            messages.success(request, "選択された商品をカートから削除しました。")
    
    # ✅ どんな場合もレスポンスを返す
    return redirect('cart:cart_list')