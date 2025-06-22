from django.shortcuts import render
from django.http import JsonResponse
from products.models import Product
from stock.models import ProductStock, StockItem
from reports.models import SaleOrder, OrderItem
import json
#def make_sale(request):

def save_as_draft(request):
    try:
        data = json.loads(request.body)
        order = SaleOrder.objects.create(status=data[0])
        
        for data_product in data[1]:
            p_stock = ProductStock.objects.filter(id=data_product['stock_id']).first()
            product = Product.objects.filter(id=p_stock.product.id).first()
            quantity = data_product['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                sell_price=0,
                buy_price=0
            )
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def load_draft(request):
    data = json.loads(request.body)
    order = SaleOrder.objects.get(id=data['id'])
    items = OrderItem.objects.filter(order=order)
    response = []
    items_unloaded = 0
    messages = []
    for item in items:
        if item.product:
            p_stock = ProductStock.objects.filter(product=item.product).first()
            if item.quantity <= p_stock.stock:
                response.append({
                    "id": item.product.id,
                    "name": item.product.name,
                    "sell_price": item.product.sell_price,
                    "quantity": item.quantity,
                    "stock": p_stock.stock,
                    "p_stock_id": p_stock.id
                })
            else:
                messages.append("El producto "+item.product.name+" no tiene suficiente inventario para cargar está orden.")
                items_unloaded += 1
        else:
            items_unloaded += 1
    if items_unloaded == 0:
        return JsonResponse({'status': 'success', "products": response})
    else:
        return JsonResponse({'status': 'error', "items_unloaded": items_unloaded, "messages": messages, "products": response})

