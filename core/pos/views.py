from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Vendor
from stock.models import ProductStock, StockItem
import json
def index(request):
    return render(request, "pos/index.html")

def get_vendor(request):
    vendor = list(Vendor.objects.values_list("id", "name", "numberPhone"))
    return JsonResponse({'data': vendor})

def get_products(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vendor = Vendor.objects.get(id=data.get('id'))
        products_stock = ProductStock.objects.filter(product__vendor_id = vendor).select_related('product')
        if products_stock:
            data = [[
                item.id,
                item.product.name,
                item.product.price,
                item.stock
            ]for item in products_stock]
            return JsonResponse({'status': 'success', 'data': data})
        else:
            return JsonResponse({'status': 'error'})

def add_stock(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_stock = ProductStock.objects.get(id=data.get('id'))
        if product_stock:
            price = data.get('price')
            amount = data.get('amount')
            new_stock = StockItem.objects.create(product_stock = product_stock, quantity = amount, buy_price = price)
            if new_stock:
                product_stock.stock = product_stock.total_stock()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error'})
        else:
            return JsonResponse({'status': 'error'})