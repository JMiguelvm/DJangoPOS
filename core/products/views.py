from django.shortcuts import render, redirect
from products.models import Product
from vendors.models import Vendor
from categorys.models import Category
from stock.models import ProductStock, StockItem
from datetime import datetime
from django.utils import timezone

def index(request):
    products = Product.objects.all()
    return render(request, "products/index.html", {"products": products})

def edit(request):
    # Main view
    if request.method == "GET" and request.GET.get('id'):
        vendors = Vendor.objects.all()
        categorys = Category.objects.all()
        product = Product.objects.get(id=request.GET.get('id'))
        return render(request, "products/edit.html", {"product": product, "vendors": vendors, "categorys": categorys})
    # Edit case
    elif request.method == "POST" and request.POST['id']:
        product = Product.objects.get(id=request.POST['id'])
        product.name = request.POST['name']
        product.sell_price = request.POST['price']
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id) if category_id and category_id.isdigit() else None
        vendor_id = request.POST.get("vendor")
        vendor = Vendor.objects.get(id=vendor_id) if vendor_id and vendor_id.isdigit() else None
        product.description = request.POST['description']
        product.bar_code = request.POST['bar_code']
        product.save()
        return redirect('products:index')
    # Delete case
    elif request.method == "GET" and request.GET.get('delete'):
        product = Product.objects.get(id=request.GET.get('delete'))
        product.delete()
        return redirect('products:index')
    # If not exist
    else:
        return redirect('products:index')

def create(request):
    vendors = Vendor.objects.all()
    categorys = Category.objects.all()
    current_datetime = timezone.now().strftime('%Y-%m-%dT%H:%M')
    
    if request.method == "POST":
        name = request.POST['name']
        
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id) if category_id and category_id.isdigit() else None
        
        vendor_id = request.POST.get("vendor")
        vendor = Vendor.objects.get(id=vendor_id) if vendor_id and vendor_id.isdigit() else None

        sell_price = request.POST['price']
        description = request.POST['description']
        bar_code = request.POST.get('bar_code')
        
        product = Product.objects.create(
            name=name,
            category=category,
            sell_price=sell_price,
            vendor=vendor,
            description=description,
            bar_code=bar_code
        )
        
        # Inventario inicial
        if request.POST.get('initial_inv'):
            p_stock = ProductStock.objects.create(product=product)
            dt = timezone.now()
            amount = request.POST['amount']
            buy_price = request.POST['buy_price']
            StockItem.objects.create(
                product_stock=p_stock,
                quantity=amount,
                date=dt,
                buy_price=buy_price
            )
            p_stock.stock = p_stock.total_stock()
            p_stock.save()
        
        return redirect('products:index')
    
    return render(request, "products/create.html", {"vendors": vendors, "categorys": categorys, "datetime": current_datetime})
