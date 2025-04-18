from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Vendor
from stock.models import ProductStock
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
            data = [{
                'id': item.id,
                'name': item.product.name,
                'price': item.product.price,
                'stock': item.stock
            }for item in products_stock]
            return JsonResponse({'status': 'success', 'data': data})
        else:
            return JsonResponse({'status': 'error'})