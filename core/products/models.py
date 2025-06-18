from django.db import models
from vendors.models import Vendor
from categorys.models import Category
class Product(models.Model):
    name = models.CharField(max_length=128)
    sell_price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    iva = models.BooleanField(default=True)
    description = models.TextField(null=True, default=None)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, default=None)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=None)
    bar_code = models.CharField(max_length=20, default=0)

    def __str__(self):
        return f"{self.id} - {self.name}"