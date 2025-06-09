from django.db import models
from vendors.models import Vendor
from categorys.models import Category
class Product(models.Model):
    name = models.CharField(max_length=128)
    sell_price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(null=True, default=None)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    bar_code = models.CharField(max_length=20, default=0)

    def __str__(self):
        return self.name