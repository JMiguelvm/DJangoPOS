from django.db import models
from django.utils import timezone
from products.models import Product

class ProductStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.product.name} - ID PS: {self.id}- {self.product.id}- {self.stock}"
    def total_stock(self):
        total = sum(
            item.quantity
            for item in self.stockitem_set.filter(voided=False)
        )
        self.stock = total
        self.save(update_fields=['stock'])
        return total

class StockItem(models.Model):
    product_stock = models.ForeignKey(ProductStock, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    quantity_used = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    buy_price = models.IntegerField(default=0) # Whitout taxes
    voided = models.BooleanField(default=False)
    is_depleted = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.product_stock.id} - {self.quantity}"
