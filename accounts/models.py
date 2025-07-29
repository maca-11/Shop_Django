from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from shopsite.models import Product  # 商品モデルのインポート

class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.purchased_at})"