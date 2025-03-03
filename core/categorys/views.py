from django.shortcuts import render

def index(request):
    return render(request, "categorys/index.html")

def edit(request):
    return render(request, "categorys/edit.html")