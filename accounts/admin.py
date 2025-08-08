
# Register your models here.
from django.contrib import admin
from .models import PurchaseHistory

class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'purchased_at', 'total_price')

admin.site.register(PurchaseHistory, PurchaseHistoryAdmin)