from django.contrib import admin

from .models import ProductStock, StockItem

admin.site.register(ProductStock)
admin.site.register(StockItem)