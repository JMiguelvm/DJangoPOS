from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Vendor
from django.db.models import Subquery
from stock.models import ProductStock, StockItem
from reports.models import SaleOrder, OrderItem
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from collections import defaultdict
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
                item.product.sell_price,
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
                product_stock.save()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error'})
        else:
            return JsonResponse({'status': 'error'})

def get_product_by_barcode(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            product = Product.objects.get(bar_code=data['barcode'])
            try:
                pstock = ProductStock.objects.get(product=product)
                return JsonResponse({
                    'status': 'success',
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.sell_price,
                        'stock': pstock.stock,
                        'iva': product.iva,
                        'stock_id': pstock.id
                    }
                })
        
            except ObjectDoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Producto sin seguimiento de inventario'
                })
            
        except ObjectDoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Producto no encontrado'
            })

def get_stock(request):
    products_stock = ProductStock.objects.all()
    if products_stock:
        data = [[
            [item.id, item.product.id],
            item.product.name,
            item.product.sell_price,
            item.product.category.name if item.product.category else None,
            item.stock,
            item.product.iva
        ]for item in products_stock]
        return JsonResponse({'status': 'success', 'data': data})
    else:
        return JsonResponse({'status': 'error', 'data': []})
    

@transaction.atomic
def make_order(request):
    try:
        data = json.loads(request.body)
        order = SaleOrder.objects.create(status=data[0])
        
        for data_product in data[1]:
            p_stock = ProductStock.objects.filter(id=data_product['stock_id']).first()
            product = Product.objects.filter(id=p_stock.product.id).first()
            entries = StockItem.objects.filter(
                product_stock=p_stock, is_depleted=False
            ).order_by("date")
            
            quantity_to_sell = data_product['quantity']
            
            for entrie in entries:
                quantity_remaining = entrie.quantity - entrie.quantity_used
                if quantity_to_sell <= quantity_remaining:
                    entrie.quantity_used += quantity_to_sell
                    if entrie.quantity == entrie.quantity_used:
                        entrie.is_depleted = True
                    entrie.save()
                    
                    StockItem.objects.create(
                        product_stock=p_stock,
                        quantity=quantity_to_sell * -1,
                        buy_price=entrie.buy_price,
                        is_depleted=True
                    )
                    
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        iva=data_product['iva'],
                        quantity=quantity_to_sell,
                        sell_price=data_product['sell_price'],
                        buy_price=entrie.buy_price
                    )
                    break
                else:
                    entrie.quantity_used += quantity_remaining
                    if entrie.quantity == entrie.quantity_used:
                        entrie.is_depleted = True
                    quantity_to_sell -= quantity_remaining
                    entrie.save()
                    
                    StockItem.objects.create(
                        product_stock=p_stock,
                        quantity=quantity_remaining * -1,
                        buy_price=entrie.buy_price,
                        is_depleted=True
                    )
                    
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        iva=data_product['iva'],
                        quantity=quantity_remaining,
                        sell_price=data_product['sell_price'],
                        buy_price=entrie.buy_price
                    )
                    
                    if quantity_to_sell == 0:
                        break
            p_stock.stock = p_stock.total_stock()
            p_stock.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def get_orders(request):
    orders = SaleOrder.objects.all()
    if orders:
        data = [{
            'id': order.id,
            'date': order.date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': order.status
        }for order in orders]
        return JsonResponse({'status': 'success', 'data': data})
    else:
        return JsonResponse({'status': 'error', 'data': []})

def get_specific_order(request):
    data = json.loads(request.body)
    order = SaleOrder.objects.filter(id=data['id']).first()
    order_items = OrderItem.objects.filter(order=order)
    items = defaultdict(lambda: {
        'product_name': '',
        'quantity': 0,
        'sell_price': 0,
        'total': 0,
        'iva': 0,
    })
    for item in order_items:
        key = item.product.id
        items[key]['product_name'] = item.product.name
        items[key]['quantity'] += item.quantity
        items[key]['sell_price'] = item.sell_price
        items[key]['total'] += item.quantity*item.sell_price
        items[key]['iva'] = item.iva
        

    data = {
        'order': {
            'id': order.id,
            'date': order.date.strftime('%#d de %B de %Y a las %H:%M').capitalize(),
            'status': order.status
        },
        'items': [
            {'order_item': item}for item in items.values()
        ]
    }
    return JsonResponse(data)