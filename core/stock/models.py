from django.db import models
from django.utils import timezone
from products.models import Product

class ProductStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.product.name} - {self.stock}"

class StockItem(models.Model):
    product_stock = models.ForeignKey(ProductStock, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    buy_price = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.product_stock.id} - {self.quantity}"
