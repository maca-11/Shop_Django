from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from shopsite.models import Product  # 商品管理アプリからインポート

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items_for_cart')

    quantity = models.IntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity