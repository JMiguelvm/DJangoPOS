from django.contrib import admin
from .models import OrderItem, SaleOrder, SaleReport

# Register your models here.
admin.site.register(OrderItem)
admin.site.register(SaleReport)
admin.site.register(SaleOrder)