from django.db import models
from django.utils import timezone
from products.models import Product
from customers.models import Customer

class SaleReport(models.Model):
    options = [
        (1, "Diario"),
        (2, "Semanal"),
        (3, "Mensual")
    ]
    type = models.IntegerField(choices=options, default=None, null=True)
    date = models.DateTimeField(null=True) # Siempre date pertenece a el primer día
    amount = models.IntegerField()
    def __str__(self):
        return f"{self.date.date()} /-/ {self.amount} /-/ {self.options[self.type - 1]}"
    
class SaleOrder(models.Model):
    options = [
        (1, "Borrador"),
        (2, "Publicada"),
        (3, "Anulada")
    ]
    date = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, default=None)
    status = models.IntegerField(choices=options, default=1)
    registered = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.date} /-/ {self.options[self.status-1][1]}"

class OrderItem(models.Model):
    order = models.ForeignKey(SaleOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_price = models.IntegerField(default=0)