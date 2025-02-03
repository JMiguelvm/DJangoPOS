from django.contrib import admin
from .models import Product, Vendor, Category, Customer, Debt, SaleOrder, OrderItem, ProductStock, SaleReport

# Register your models here.

admin.site.register(Product)
admin.site.register(Vendor)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Debt)
admin.site.register(SaleOrder)
admin.site.register(OrderItem)
admin.site.register(ProductStock)
admin.site.register(SaleReport)