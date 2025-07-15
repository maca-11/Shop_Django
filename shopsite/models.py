from django.db import models
from django.contrib.auth.models import User # Userモデルをインポート

# Create your models here.
class Category(models.Model):
    name = models.CharField("ジャンル名", max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name="ジャンル", on_delete=models.CASCADE)
    name = models.CharField("商品名", max_length=255)
    description = models.TextField("商品説明", blank=True, null=True)
    price = models.DecimalField("価格", max_digits=10, decimal_places=2)
    stock = models.IntegerField("在庫数", default=0)

    def __str__(self):
        return self.name
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("数量", default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} のカート: {self.product.name}"
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField("合計金額", max_digits=10, decimal_places=2)
    used_points = models.PositiveIntegerField("使用ポイント", default=0)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("数量")
    price = models.DecimalField("価格", max_digits=10, decimal_places=2)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField("保有ポイント", default=0)

    def __str__(self):
        return f"{self.user.username} - {self.points} ポイント"
    

from django.urls import reverse # reverse関数をインポート

class Article(models.Model):
    # その投稿の詳細ページへのリンク
    def get_absolute_url(self):
        return reverse("shopsite:detail", kwargs={"pk": self.pk})