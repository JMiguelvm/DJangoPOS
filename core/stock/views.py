from django.shortcuts import render

def index(request):
    return render(request, "stock/index.html")

def edit(request):
    return render(request, "stock/edit.html")

def create(request):
    return render(request, "stock/create.html")