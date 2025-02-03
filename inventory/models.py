from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# Create your models here.


class Vendor(models.Model):
    name = models.CharField(max_length=128)
    numberPhone = models.IntegerField(null=True, default=None)
    description = models.TextField(null=True, default=None)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=128)
    icon = models.CharField(max_length=128, null=True, default=None)
    description = models.TextField(null=True, default=None)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField(default=0.0)
    sell_price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(null=True, default=None)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    bar_code = models.CharField(max_length=20, default=0)

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Debt(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    amount = models.FloatField()
    date = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return f"{self.customer} — {self.amount}"
    
class SaleOrder(models.Model):
    options = [
        (1, "Borrador"),
        (2, "Publicada"),
        (3, "Eliminada")
    ]
    date = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=options, default=1)
    registered = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.date} /-/ {self.options[self.status-1][1]}"

class OrderItem(models.Model):
    order = models.ForeignKey(SaleOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_price = models.IntegerField(default=0) #Consulta el precio actual de compra del producto

class ProductStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    buy_price = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


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