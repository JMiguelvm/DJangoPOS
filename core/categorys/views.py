from django.shortcuts import render, redirect
from categorys.models import Category

def index(request):
    categorys = Category.objects.all()
    return render(request, "categorys/index.html", {"categorys": categorys})

def edit(request):
    # Main view
    if request.method == "GET" and request.GET.get('id'):
        category = Category.objects.get(id=request.GET.get('id'))
        return render(request, "categorys/edit.html", {"category": category})
    # Edit case
    elif request.method == "POST" and request.POST['id']:
        category = Category.objects.get(id=request.POST['id'])
        name = request.POST['name']
        description = request.POST['description']
        category.name = name
        category.description = description
        category.save()
        return redirect('categorys:index')
    # Delete case
    elif request.method == "GET" and request.GET.get('delete'):
        category = Category.objects.get(id=request.GET.get('delete'))
        category.delete()
        return redirect('categorys:index')
    # If not exist
    else:
        return redirect('categorys:index')

def create(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        Category.objects.create(name=name, description=description)
        return redirect('categorys:index')
    return render(request, "categorys/create.html")