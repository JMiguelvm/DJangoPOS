from django.shortcuts import render, redirect
from vendors.models import Vendor

def index(request):
    vendors = Vendor.objects.all()
    return render(request, "vendors/index.html", {"vendors": vendors})

def edit(request):
    # Main view
    if request.method == "GET" and request.GET.get('id'):
        vendor = Vendor.objects.get(id=request.GET.get('id'))
        return render(request, "vendors/edit.html", {"vendor": vendor})
    # Edit case
    elif request.method == "POST" and request.POST['id']:
        vendor = Vendor.objects.get(id=request.POST['id'])
        name = request.POST['name']
        number = request.POST['number']
        description = request.POST['description']
        vendor.name = name
        vendor.numberPhone = number
        vendor.description = description
        vendor.save()
        return redirect('vendors:index')
    # Delete case
    elif request.method == "GET" and request.GET.get('delete'):
        vendor = Vendor.objects.get(id=request.GET.get('delete'))
        vendor.delete()
        return redirect('vendors:index')
    # If not exist
    else:
        return redirect('vendors:index')

def create(request):
    if request.method == "POST":
        name = request.POST['name']
        number = request.POST['numberP']
        description = request.POST['description']
        Vendor.objects.create(name=name, numberPhone=number, description=description)
        return redirect('vendors:index')
    return render(request, "vendors/create.html")