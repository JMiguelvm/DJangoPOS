from django.shortcuts import render, redirect
from products.models import Product
from vendors.models import Vendor
from categorys.models import Category

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
        product.iva = True if request.POST.get("iva") else False
        product.category = Category.objects.get(id=request.POST['category'])
        product.vendor = Vendor.objects.get(id=request.POST['vendor'])
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
    if request.method == "POST":
        name = request.POST['name']
        category = Category.objects.get(id=request.POST['category'])
        sell_price = request.POST['price']
        iva = True if request.POST.get("iva") else False
        vendor = Vendor.objects.get(id=request.POST['vendor'])
        description = request.POST['description']
        bar_code = request.POST.get('bar_code')
        Product.objects.create(name=name, category=category, sell_price=sell_price, iva=iva, vendor=vendor, description=description, bar_code=bar_code)
        return redirect('products:index')
    return render(request, "products/create.html", {"vendors": vendors, "categorys": categorys})