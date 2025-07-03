from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Subquery
from .models import ProductStock, StockItem, Product
from datetime import datetime
from django.utils import timezone

def index(request):
    pstock = ProductStock.objects.all()
    return render(request, "stock/index.html", {"pstock": pstock})

def edit(request):
    product_s = ProductStock.objects.get(id=request.GET.get('product_s'))
    current_datetime = timezone.now().strftime('%Y-%m-%dT%H:%M')
    items = product_s.stockitem_set.all()
    for item in items:
        item.total = item.buy_price * item.quantity
    return render(request, "stock/edit.html", {"product_s": product_s, "items": items, "datetime": current_datetime})

def create(request):
    products_in_stock = ProductStock.objects.values('product')
    # Exclude product has stock instance from product stock creation list
    products = Product.objects.exclude(id__in=Subquery(products_in_stock))
    # Create Product stock
    if request.GET.get('product'):
        product = Product.objects.get(id=request.GET.get('product'))
        ProductStock.objects.create(product=product)
        return redirect('stock:index')
    # Delete Product stock
    if request.GET.get('delete_s'):
        product_s = ProductStock.objects.get(id=request.GET.get('delete_s'))
        messages.success(request, f'Inventario de producto "{product_s.product.name}" eliminado con éxito.')
        product_s.delete()
        return redirect('stock:index')
    # Create stock item
    if request.POST and request.POST.get('price'):
        datetime_str = request.POST.get('datetime')
        if datetime_str:
            try:
                dt = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                dt = timezone.now()
        product_s = ProductStock.objects.get(id=request.POST['id'])
        amount = request.POST['amount']
        price = request.POST['price']
        # Add stock
        messages.success(request, "Inventario añadido con éxito.")
        StockItem.objects.create(product_stock=product_s, quantity=amount, date=dt, buy_price=price)
        product_s.stock = product_s.total_stock()
        product_s.save()
        return redirect(reverse('stock:edit') + f'?product_s={product_s.id}')
    # Cancel stock item
    if request.GET.get('void'):
        item = StockItem.objects.get(id=request.GET.get('void'))
        # Verify integrity of stock
        if (item.product_stock.total_stock() - item.quantity >= 0):
            product_s = ProductStock.objects.get(id=item.product_stock.id)
            product_s.stock = product_s.total_stock() - item.quantity
            product_s.save()
            item.voided = True
            item.save()
            messages.success(request, f'Item anulado con éxito.')
        else:
            messages.error(request, f'No se puede anular este registro.')
        return redirect(reverse('stock:edit') + f'?product_s={item.product_stock.id}')
    return render(request, "stock/create.html", {"products": products})