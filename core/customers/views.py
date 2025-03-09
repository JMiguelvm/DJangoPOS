from django.shortcuts import render

def index(request):
    return render(request, "customers/index.html")

def edit(request):
    return render(request, "customers/edit.html")

def create(request):
    return render(request, "customers/create.html")