from django.shortcuts import render

def index(request):
    return render(request, "products/index.html")

def edit(request):
    return render(request, "products/edit.html")

def create(request):
    return render(request, "products/create.html")